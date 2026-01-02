from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from products.serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    CartSerializer,
)
from products.models import Product, Cart, ProductCategory, Order, OrderItems


@api_view(["GET"])
def api_prodcuts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["GET"])
def api_category(request):
    categories = ProductCategory.objects.all()
    serializer = ProductCategorySerializer(categories, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def api_prodcut(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        product.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    else:
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def api_category(request, id):
    try:
        category = ProductCategory.objects.get(id=id)
    except ProductCategory.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductCategorySerializer(category, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = ProductCategorySerializer(
            category, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        category.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    else:
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def api_cart(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id, user=request.user)
    except Cart.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CartSerializer(cart, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        cart.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    else:
        return Response(status.HTTP_400_BAD_REQUEST)
