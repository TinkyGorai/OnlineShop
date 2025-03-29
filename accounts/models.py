from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid 
from base.emails import send_account_verification_mail
from products.models import Product, ProductColorVariant,ProductSizeVariant

# Profile Model
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_Email_verified = models.BooleanField(default=True)
    email_token = models.CharField(max_length=150, blank=True, null=True)
    Profile_Image = models.ImageField(upload_to='profile', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_cart_count(self):
        return CartItems.objects.filter(cart__user=self.user, cart__is_paid=False).count()

# Coupon Model
class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=50, null=True)
    is_expired = models.BooleanField(default=False)
    discount_amount = models.IntegerField(blank=True)
    minimum_amount = models.IntegerField(blank=True)

# Cart Model
class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True, related_name="coupon")
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

    def get_cart_total(self):
        total_price = 0

        for item in self.cart_items.all():
            base_price = item.products.base_price if item.products else 0
            size_price = item.size_variant.additional_price if item.size_variant else 0
            color_price = item.color_variant.additional_price if item.color_variant else 0
            total_price += base_price + size_price + color_price

        # Apply coupon discount if applicable
        if self.coupon and total_price >= self.coupon.minimum_amount:
            return total_price - self.coupon.discount_amount

        return total_price

    def __str__(self):
        return self.user.username

# Cart Items Model
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='cart_items')
    products = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    size_variant = models.ForeignKey(ProductSizeVariant, on_delete=models.SET_NULL, blank=True, null=True)
    color_variant = models.ForeignKey(ProductColorVariant, on_delete=models.SET_NULL, blank=True, null=True)

    def get_product_price(self):
        base_price = self.products.base_price if self.products else 0
        size_price = self.size_variant.additional_price if self.size_variant else 0
        color_price = self.color_variant.additional_price if self.color_variant else 0
        return base_price + size_price + color_price

# Signals for user profile & cart creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Cart.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
