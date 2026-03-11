from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.api_login, name="api_login"),
    path("signup/", views.api_signup, name="api_signup"),
    path("logout", views.api_logout, name="api_logout"),
    path("users/", views.user_list, name="api_users"),
    path("user-detail/", views.user_detail, name="api_user_detail"),
]
