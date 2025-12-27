from django.contrib import admin

from .models import (
    Product,
    ProductCategory,
    ProductImage,
    Discount,
    Order,
    OrderItems,
    Cart,
    Review,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductImage)
admin.site.register(Discount)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Cart)
admin.site.register(Review)
