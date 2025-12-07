from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from pprint import pprint
from django.http import HttpResponse

from .models import Product, Cart, ProductCategory, Order, OrderItems, Review
from users.models import UserAddress, CustomUser


def calc_discount_amt(product):
    if product.discount:
        discount_percent = product.discount.discount_percent
        discount_amount = product.price - (
            product.price * (discount_percent / 100)
        )
        return discount_amount
    return None


def home(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()

    # cart_items = Cart.objects.filter(user=request.user)
    # cart_items_count = len([item for item in cart_items])
    # print(cart_items_count)

    discount_amts = [calc_discount_amt(product) for product in products]

    return render(
        request,
        "products/home.html",
        {
            "products": products,
            "discount_amts": discount_amts,
            "categories": categories,
            # "cart_items_count": cart_items_count,
        },
    )


def search(request):
    if request.method == "POST":
        query = request.POST.get("query")
        results = (
            Product.objects.filter(Q(name__icontains=query)) if query else []
        )
        return render(
            request,
            "products/search_result.html",
            {"results": results, "query": query},
        )
    return redirect("home")


def product_by_category(request, slug):
    products = Product.objects.filter(category__slug=slug)
    category = ProductCategory.objects.get(slug=slug)

    return render(
        request,
        "products/products.html",
        {"products": products, "category": category},
    )


def product_detail(request, slug):
    discount_amount = None

    product = Product.objects.get(slug=slug)
    discount_amount = calc_discount_amt(product)

    similar_products = Product.objects.filter(category=product.category)
    similar_products = [prod for prod in similar_products if prod != product]

    reviews = get_reviews(slug)
    pprint(reviews)

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "discount_amt": discount_amount,
            "similar_products": similar_products,
            "reviews": reviews,
        },
    )


def products_page(request):
    product_by_category = {}
    categories = ProductCategory.objects.all()

    for category in categories:
        product_by_category[category] = Product.objects.filter(
            category=category
        )

    print(product_by_category)

    return render(
        request,
        "products/products_page.html",
        {"product_by_category": product_by_category},
    )


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            product_id_id=product_id, user=request.user
        )

        cart_item.save()
        return redirect("cart")
    else:
        return redirect("login")


@login_required
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(
            product_id_id=product_id, user=request.user
        )

        cart_item.delete()
        return redirect("cart")
    else:
        return redirect("login")


@login_required
def cart(request):
    total = 0
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists:
        return render(request, "products/cart.html", {"cart_items": []})

    for item in cart_items:
        item.total = item.quantity * item.product_id.price
        total += item.total
        item.save()

    return render(
        request,
        "products/cart.html",
        {"cart_items": cart_items, "total": total},
    )


@login_required
def order(request):
    # first_name = request.POST.get("first_name")
    # last_name = request.POST.get("last_name")
    # address = request.POST.get("address")
    # phone_number = request.POST.get("phone_number")

    user = CustomUser.objects.get(id=request.user.id)
    # user.phone_no = phone_number
    # user.first_name = first_name
    # user.last_name = last_name
    # user.save()

    UserAddress.objects.get_or_create(user=user)

    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect("home")

    order = Order.objects.create(user=request.user, total=0)
    total = 0

    for item in cart_items:
        OrderItems.objects.create(
            order_id=order,
            quantity=item.quantity,
            product_id=item.product_id,
        )
        total += item.product_id.price * item.quantity

    order.total = total
    order.save()

    order_items = OrderItems.objects.filter(order_id=order)

    # deduct from the stock
    for item in cart_items:
        product = Product.objects.get(id=item.product_id.id)
        product.quantity = product.quantity - item.quantity
        product.save()

    cart_items.delete()

    return render(
        request,
        "products/payment.html",
        {"order_items": order_items, "order": order},
    )


def payment_success(request):
    return render(request, "products/success.html")


def checkout(request):
    total = 0
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists:
        return render(request, "products/cart.html", {"cart_items": []})

    for item in cart_items:
        total += item.total

    user_address = UserAddress.objects.filter(user=request.user)
    # user = CustomUser.objects.filter(user=request.user).first()

    if not user_address.exists():
        user_address = None
    else:
        user_address = user_address.first()

    return render(
        request,
        "products/checkout.html",
        {
            "cart_items": cart_items,
            "product": None,
            "total": total,
            "user_address": user_address,
            "user": request.user,
        },
    )


def direct_order(request, product_id):
    product = Product.objects.get(id=product_id)
    total = product.price

    return render(
        request,
        "products/checkout.html",
        {"product": product, "cart_items": None, "total": total},
    )


def update_qunatity(request, product_id, operation, to):
    print(operation)
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists:
        return redirect(to)

    cart_item = Cart.objects.get(product_id=product_id)
    if operation == "+":
        cart_item.quantity += 1

    if operation == "-":
        if cart_item.quantity == 1:
            return redirect(to)
        cart_item.quantity -= 1

    cart_item.save()

    return redirect(to)


def get_reviews(slug):
    # only one level of nesting of review
    reviews = Review.objects.filter(product__slug=slug)
    _reviews = []
    for review in reviews:
        if review.reply:
            continue

        new = review.__dict__
        replies = Review.objects.filter(reply=review)
        user = CustomUser.objects.filter(id=review.user.id).first()

        if user:
            new["user"] = user

        if replies:
            new["replies"] = replies

        _reviews.append(new)

    return _reviews


def write_review(request, id, slug):
    if request.method == "POST":
        comment = request.POST.get("comment")

        product = Product.objects.filter(slug=slug).first()
        if not product:
            return HttpResponse("Successful Failed")

        reply = Review.objects.filter(id=id).first()

        review = Review.objects.create(
            product=product, user=request.user, comment=comment, reply=reply
        )

        review.save()

        return redirect("product_detail", slug=slug)
