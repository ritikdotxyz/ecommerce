from rest_framework import serializers

from products.models import (
    ProductCategory,
    Discount,
    Product,
    ProductImage,
    Cart,
    Order,
    OrderItems,
)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"

    def validate(self, data):
        if data["name"].stip() == "":
            raise serializers.ValidationError(
                "Name cannot be empty or whitespace only"
            )


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data):
        if data["name"].stip() == "":
            raise serializers.ValidationError(
                "Name cannot be empty or whitespace only"
            )

        if data["price"] < 0:
            raise serializers.ValidationError("Price cannot be negative")

        if data["quantity"] < 0:
            raise serializers.ValidationError("Quantity cannot be negative")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"
