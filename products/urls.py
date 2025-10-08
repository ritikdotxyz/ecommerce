from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product/<int:id>", views.product_detail, name="product_detail"),
    path("products/", views.products_page, name="products_page"),
    path("cart/", views.cart, name="cart"),
    path("order/", views.order, name="order"),
    path("add-to-cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path(
        "remove-from-cart/<int:product_id>",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/<int:product_id>", views.direct_order, name="direct_checkout"),
    path(
        "products/category/<int:category_id>",
        views.product_by_category,
        name="products_category",
    ),
    path(
        "update_quantity/<int:product_id>/<str:operation>/<str:to>/",
        views.update_qunatity,
        name="update_quantity",
    ),
    path("search", views.search, name="search"),
    path("api/products/", views.api_prodcuts, name="api_products"),
    path("api/categories/", views.api_category, name="api_categories"),
    path("api/product/<int:id>/", views.api_prodcut, name="api_product"),
    path("api/category/<int:id>/", views.api_category, name="api_category"),
    path("api/cart/<int:cart_id>/", views.api_cart, name="api_cart"),


]
