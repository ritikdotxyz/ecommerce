from rest_framework import serializers
from users.models import CustomUser, UserAddress


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_no", "password"]


class UserAddressSerializer(serializers.Serializer):
    class Meta:
        models = UserAddress
        fields = ["user", "address_1", "address_2", "city"]
