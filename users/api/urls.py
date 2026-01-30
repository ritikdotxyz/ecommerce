from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.api_login, name="api_login"),
    path("signup/", views.api_signup, name="signup"),
    path("logout", views.api_logout, name="logout"),
    path("users/", views.user_list, name="users"),
    path("user-detail/", views.user_detail, name="user-detail"),
]
