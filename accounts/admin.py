from django.contrib import admin
from .models import Profile,Cart,CartItems,Coupon,Order,OrderItem
# Register your models here
admin.site.register(Coupon)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)
class OrderItemVariantInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemVariantInline]

admin.site.register(Order, OrderAdmin)