from django.urls import path, include

from . import views


urlpatterns = [
    path("api/", include("products.api.urls")),
    path("", views.home, name="home"),
    path("product/<str:slug>", views.product_detail, name="product_detail"),
    path("products/", views.products_page, name="products_page"),
    path("cart/", views.cart, name="cart"),
    path("order/", views.order, name="order"),
    path(
        "add-to-cart/<int:product_id>", views.add_to_cart, name="add_to_cart"
    ),
    path(
        "remove-from-cart/<int:product_id>",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "checkout/<int:product_id>", views.direct_order, name="direct_checkout"
    ),
    path(
        "products/category/<str:slug>",
        views.product_by_category,
        name="products_category",
    ),
    path(
        "update_quantity/<int:product_id>/<str:operation>/<str:to>/",
        views.update_qunatity,
        name="update_quantity",
    ),
    path("search", views.search, name="search"),
    path("success/", views.payment_success, name="success"),
    path(
        "review/<int:id>/<str:slug>", views.write_review, name="write_review"
    ),
    path("cart-item-count/", views.get_cart_count, name="cart-item-count"),
    path("order-history/", views.order_history, name="order_history"),
    path("order-detail/<int:id>/", views.order_detail, name="order_detail"),
]
