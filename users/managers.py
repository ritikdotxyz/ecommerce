from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(gettext_lazy("The email must be set."))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and save a SuperUser with the given email and password.
        """
        if not email:
            raise ValueError(gettext_lazy("The email must be set."))

        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(gettext_lazy("Superuser must have is_staff=True."))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(gettext_lazy("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **kwargs)
