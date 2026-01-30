from rest_framework import serializers
from users.models import CustomUser, UserAddress


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_no", "password"]

    def validate(self, data):
        if len(data["password"]) > 16 and len(data["password"]) < 8:
            raise serializers.ValidationError(
                "Password length should be between 8 to 16"
            )

        return data


class UserAddressSerializer(serializers.Serializer):
    class Meta:
        models = UserAddress
        fields = ["user", "address_1", "address_2", "city"]
