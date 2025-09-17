from django.contrib import admin

from .models import *


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)
admin.site.register(Discount)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Cart)
