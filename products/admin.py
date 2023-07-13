from django.contrib import admin
from .models import Category
from .models import Product
from .models import ProductImage,SizeVariant,ColorVariant


# Register your models here.
class ProductImageAdmin(admin.StackedInline):
    model=ProductImage
@admin.register(SizeVariant)
class SizevariantAdmin(admin.ModelAdmin):
    list_display=['size','price']
    model=SizeVariant
@admin.register(ColorVariant)
class ColorvariantAdmin(admin.ModelAdmin):
    list_display=['color','price']
    model=ColorVariant

class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','price']
    inlines=[ProductImageAdmin]



admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
