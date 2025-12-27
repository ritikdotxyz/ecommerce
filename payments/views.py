import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from decimal import Decimal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from products.models import (
    Product,
    Cart,
    Order,
    OrderItems,
)
from users.models import UserAddress, CustomUser

stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = settings.DOMAIN


def handle_user_info(request):
    user = CustomUser.objects.get(id=request.user.id)

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


def checkout_session(request):
    if request.method == "POST":
        try:
            # Get the product details from the POST request
            # product_name = request.POST.get("name")
            print("price: ", request.POST.get("price"))
            product_price = (
                Decimal(request.POST.get("price")) * 100
            )  # Convert to cents for Stripe
            print(product_price)
            # product_description = request.POST.get("description")

            user_email = request.user.email

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "npr",
                            "product_data": {
                                "name": "E-commerce Product",
                            },
                            "unit_amount": int(product_price),
                        },
                        "quantity": 1,
                    },
                ],
                metadata={"product_id": 1},
                mode="payment",
                success_url=DOMAIN + "/success/",
                cancel_url=DOMAIN + "/cancel/",
                customer_email=user_email,
            )

            return redirect(checkout_session.url)
        except Exception as error:
            return render(request, "payments/error.html", {"error": error})

    return render(request, "payments/cancel.html")


def success(request):
    handle_user_info(request)
    return render(request, "payments/success.html")


def cancel(request):
    return render(request, "payments/cancel.html")


@csrf_exempt
def stripe_webhook(request):

    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = settings.WEBHOOK_ENDPOINT_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        print(event)
        print("Payment was successful.")

    return HttpResponse(status=200)
