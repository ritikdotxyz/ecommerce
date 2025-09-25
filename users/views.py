from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .forms import CustomerCreationForm, LoginForm
from .serializers import CustomUserSerializer


@api_view(["POST"])
def api_login(request):
    email = request.data["email"]
    password = request.data["password"]
    user = authenticate(request, email=email, password=password)

    if user:
        return Response({"message": "Login Successful"}, status=status.HTTP_200_OK)
    return Response({"message": "Failed to login"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def api_signup(request):
    if request.method == "POST":
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User Successfully created.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def user_list(request):
    if request.method == "GET":
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    if request.method == "POST":
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def user_detail(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)


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
