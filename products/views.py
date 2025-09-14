from django.shortcuts import render

from .models import Product


def calc_discount_amt(product):
    if product.discount:
        discount_percent = product.discount.discount_percent
        discount_amount = product.price - (product.price * (discount_percent / 100))
        return discount_amount
    return None


def home(request):
    products = Product.objects.all()

    discount_amts = [calc_discount_amt(product) for product in products]
        
    return render(request, "products/home.html", {"products": products, "discount_amts": discount_amts})


def product_detail(request, id):
    discount_amount = None

    product = Product.objects.get(id=id)
    discount_amount = calc_discount_amt(product)
    
    return render(request, "products/product_detail.html", {"product": product, "discount_amt": discount_amount})


def products_page(request):
    return render(request, "products/products_page.html")


def cart(request):
    return render(request, "products/cart.html")


def order(request):
    return render(request, "products/order.html")