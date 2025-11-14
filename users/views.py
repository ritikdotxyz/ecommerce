from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
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
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect("home")
            else:
                message = "Invalid email or password"

    return render(
        request, "users/login.html", {"form": form, "message": message}
    )


def signup(request):

    message = ""

    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            message = list(form.errors.values())[-1]

    else:
        form = CustomerCreationForm()
    return render(
        request, "users/signup.html", {"form": form, "message": message}
    )


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
    return render(
        request,
        "users/profile.html",
        {"user": user, "user_address": user_address},
    )
