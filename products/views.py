from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Cart, ProductCategory


def calc_discount_amt(product):
    if product.discount:
        discount_percent = product.discount.discount_percent
        discount_amount = product.price - (product.price * (discount_percent / 100))
        return discount_amount
    return None


def home(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()

    discount_amts = [calc_discount_amt(product) for product in products]

    return render(
        request,
        "products/home.html",
        {"products": products, "discount_amts": discount_amts, "categories": categories},
    )


def product_detail(request, id):
    discount_amount = None

    product = Product.objects.get(id=id)
    discount_amount = calc_discount_amt(product)

    return render(
        request,
        "products/product_detail.html",
        {"product": product, "discount_amt": discount_amount},
    )


def products_page(request):
    return render(request, "products/products_page.html")


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            product_id_id=product_id, user=request.user
        )

        cart_item.save()
        return redirect("cart")
    else:
        return redirect("login")
    
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
        total += item.product_id.price
    
    return render(request, "products/cart.html", {"cart_items": cart_items, "total":total})


def order(request):
    return render(request, "products/order.html")


def checkout(request):
    total = 0
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists:
        return render(request, "products/cart.html", {"cart_items": []})
    
    for item in cart_items:
        total += item.product_id.price

    print(cart_items)
    return render(request, "products/checkout.html", {"cart_items": cart_items, "product":None, "total":total})


def direct_order(request, product_id):
    product = Product.objects.get(id=product_id)
    total = product.price

    return render(request, "products/checkout.html", {"product": product,  "cart_items": None, "total":total})
