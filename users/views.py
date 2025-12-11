from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import UserAddress
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


def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")

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


def contact(request):
    return render(request, "contact.html")


def profile_edit(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address_1 = request.POST.get("address_1")
        address_2 = request.POST.get("address_2")
        phone_number = request.POST.get("phone")
        city = request.POST.get("city")

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.phone_no = phone_number
        user.save()

        user_address = UserAddress.objects.get(user=request.user)
        user_address.address_1 = address_1
        user_address.address_2 = address_2
        user_address.city = city
        user_address.save()

        return redirect("profile")

    try:
        user_address = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_address = {}

    return render(
        request, "users/profile_edit.html", {"user_address": user_address}
    )
