from django.contrib import admin

from users.models import CustomUser, UserAddress

admin.site.register(CustomUser)
admin.site.register(UserAddress)
