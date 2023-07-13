from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid 
from base.emails import send_account_verification_mail
from products.models import Product,SizeVariant,ColorVariant
# Create your models here.
class Profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_Email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=150,blank=True,null=True)
    Profile_Image=models.ImageField(upload_to='profile')
    def get_cart_count(self):
        return CartItems.objects.filter(cart__user=self.user,cart__is_paid=False).count()
class Coupon(BaseModel):
    coupon_code=models.CharField(max_length=50,null=True)
    is_expired=models.BooleanField(default=False)
    discount_amount=models.IntegerField(blank=True)
    minimum_amount=models.IntegerField(blank=True)

class Cart(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart')
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,blank=True,null=True,related_name="coupon")
    is_paid=models.BooleanField(default=False)
    razor_pay_order_id=models.CharField( max_length=100,null=True,blank=True)
    razor_pay_payment_id=models.CharField( max_length=100,null=True,blank=True)
    razor_pay_payment_signature=models.CharField( max_length=100,null=True,blank=True)
    def get_cart_total(self):
        total_items=self.cart_items.all()
        tot_price=[]
        for item in total_items:
            tot_price.append(item.products.price)
            if item.size_variant:
                added_price=item.size_variant.price
                tot_price.append(added_price)
            if item.color_variant:
                added_price=item.color_variant.price
                tot_price.append(added_price)

        if self.coupon:
            print(self.coupon.discount_amount)
            if(sum(tot_price)>self.coupon.minimum_amount):
             return sum(tot_price)-self.coupon.discount_amount
        return sum(tot_price)
class CartItems(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,blank=True,null=True,related_name='cart_items')
    products=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    size_variant=models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,blank=True,null=True)
    color_variant=models.ForeignKey(ColorVariant,on_delete=models.SET_NULL,blank=True,null=True)
    
    def get_product_price(self):
        price=[self.products.price]

        if self.color_variant:
            color_variant_price=self.color_variant.price
            price.append(color_variant_price)
        if self.size_variant:
            size_variant_price=self.size_variant.price
            price.append(size_variant_price)
        return sum(price)




@receiver(post_save, sender=User)
def _post_save_receiver(sender,instance,created,**kwargs):
    try:
      if created:
        email_token=str(uuid.uuid4())
        email=instance.email
        send_account_verification_mail(email_token,email)
    except Exception as e:
        print(e)
    
