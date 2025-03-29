from django.contrib import admin
from .models import Product,ProductSizeVariant, ProductColorVariant, Category



class ProductSizeVariantInline(admin.TabularInline):
    model = ProductSizeVariant
    extra = 1  # Allows adding new variants easily

class ProductColorVariantInline(admin.TabularInline):
    model = ProductColorVariant
    extra = 1
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'base_price', 'category', 'brand', 'availability')
    inlines = [ProductSizeVariantInline,ProductColorVariantInline]
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
