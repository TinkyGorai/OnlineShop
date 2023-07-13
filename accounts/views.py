from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponseServerError,HttpResponse
from .models import Profile,Cart,CartItems,Coupon
from products.models import Product,SizeVariant,ColorVariant
import razorpay
from django.conf import settings
# Create your views here.
def login_page(request):
    print(f'request:{request.POST}')
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj=User.objects.filter(email=email)
        if(not user_obj):
           messages.warning(request,'Account Not Found')
           return redirect(request.path_info)
        else:
           if not user_obj[0].profile.is_email_verified:
              messages.warning(request,'Your Account Is Not Verified')
              return HttpResponseRedirect(request.path_info)
           else:
              user_obj=authenticate(email=email,password=password)
              if (user_obj):
                login(request,user_obj)
              else:
                messages.warning(request,'Invalid Credentials')
                return redirect('/')
    return render(request,'accounts/login.html')

def register_page(request):
    print(f'request:{request.POST}')
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj=User.objects.filter(email=email)
        if(user_obj):
           messages.warning(request,'user already exists')
           return HttpResponseRedirect(request.path_info)
        else:
           user_obj=User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password)
           user_obj.set_password(password)
           user_obj.save()
           print(messages)
           messages.success(request,'A email has been to your mail')
           return HttpResponseRedirect(request.path_info)

    return render(request,'accounts/register.html')
def cart(request):
   cart=Cart.objects.get(user=request.user,is_paid=False)
   cart_items=CartItems.objects.filter(cart=cart)
   context={
      "cart":cart,
      "cartitems":cart_items,
   }
   # for item in cart_items:
   #  print(item.size_variant)
   #  print(item.products.product_images)
   #  if item.size_variant:
   #    updated_price=item.products.product_price_by_size(item.size_variant)
   #  else:
   #    updated_price=item.products.price
   #    print(updated_price)
   if request.method=='POST':
      coupon=request.POST.get('coupon')
      coupon_obj=Coupon.objects.filter(coupon_code__icontains=coupon)
      if not coupon_obj:
         messages.warning(request,'Invalid Coupon')
         return HttpResponseRedirect(request.path_info)
      if cart.coupon:
         messages.warning(request,'Coupon Already Exists')
         return HttpResponseRedirect(request.path_info)
      if cart.get_cart_total()<coupon_obj[0].minimum_amount:
         messages.warning(request,f'total bill must be greater than{coupon_obj[0].minimum_amount}')
         return HttpResponseRedirect(request.path_info)
      if coupon_obj[0].is_expired:
         messages.warning(request,f'COUPON EXPIRED')
         return HttpResponseRedirect(request.path_info)
   #    print(updated_price)
      if cart.get_cart_total()>coupon_obj[0].minimum_amount:
         messages.success(request,'Coupon Applied')
         cart.coupon=coupon_obj[0]
         cart.save()
   client=razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))
   payment=client.order.create({'amount':cart.get_cart_total(),'currency':'INR','payment_capture':1})
   cart.razor_pay_order_id=payment['id']
   cart.save()
   context['payment']=payment
   return render(request,'accounts/cart.html',context)

def add_to_cart(request,uid):
   variant=request.GET.get('variant')
   user=request.user
   products=Product.objects.get(uid=uid)
   price= products.price
   variant=request.GET.get('variant')
   cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
   card_item=CartItems.objects.create(cart=cart,products=products)
   if variant:
      variant=request.GET.get('variant')
      size_variant=SizeVariant.objects.get(size=variant)
      card_item.size_variant=size_variant
      card_item.save()
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   
def remove_from_cart(request,cart_item_uid):
   cart_item=CartItems.objects.get(uid=cart_item_uid)
   if cart_item:
      cart_item.delete()
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_coupon(request,cart_item_uid):

   cart_item=Cart.objects.get(uid=cart_item_uid)
   cart_item.coupon=None
   cart_item.save()
   messages.success(request,'Coupon Removed')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def success(request):
   order_id=request.GET.get('order_id')
   cart=Cart.objects.get(razor_pay_order_id=order_id)
   cart.is_paid(True)
   cart.save()
   return Httpresponse('Payment Success')