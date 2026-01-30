from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.api_products, name="api_products"),
    path("category/", views.api_category, name="api_category"),
    path("product/", views.api_prodcut, name="api_product"),
    path("cart/", views.api_cart, name="api_cart"),
]
