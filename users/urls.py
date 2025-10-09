from django.urls import path

from . import views
from .api import views as api_viewws

urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.log_out, name="logout"),
    # path("users/", views.user_list, name="user_list"),
    # path("users/<int:id>", views.user_detail, name="user_detail"),

    # api
    path("users/signup/", api_viewws.api_signup, name="api_signup"),
    path("users/login/", api_viewws.api_login, name="api_login"),
    path("users/logout/", api_viewws.api_logout, name="api_logout"),
]
