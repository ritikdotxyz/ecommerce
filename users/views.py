from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser, UserAddress
from .forms import CustomerCreationForm, LoginForm


def login(request):
    form = LoginForm()
    message = ""

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            message = "Invalid username or password"
            render(request, "users/login.html", {"form": form, "message": message})

    return render(request, "users/login.html", {"form": form, "message": message})


def signup(request):
    form = CustomerCreationForm()
    message = ""

    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = CustomUser(email=email)
            user.set_password(password)

            user.save()
            return redirect("login")
        except Exception as e:
            message = "Invalid input values"
            render(request, "users/signup.html", {"form": form, "message": message})

    return render(request, "users/signup.html", {"form": form, "message": message})


def log_out(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    user = request.user
    try:
        user_address = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_address = {}
    return render(request, "users/profile.html", {"user": user, "user_address": user_address})
