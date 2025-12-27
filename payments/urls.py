from django.urls import path
from . import views

urlpatterns = [
    path("checkout_session", views.checkout_session, name="checkout_session"),
    path("success/", views.success, name="success"),
    path("cancel", views.cancel, name="cancel"),
    path("stripe_webhook", views.stripe_webhook, name="stripe_webhook"),
]
