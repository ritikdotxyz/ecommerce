from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy
from django.core.validators import MaxLengthValidator

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(gettext_lazy("email address"), unique=True)
    phone_no = models.IntegerField(null=True, validators=[MaxLengthValidator(10)])
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserAddress(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address_1 = models.TextField(max_length=100)
    address_2 = models.TextField(max_length=100, null=True)
    city = models.TextField(max_length=100)
