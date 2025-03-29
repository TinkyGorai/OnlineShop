from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponseServerError,HttpResponse
from .models import Profile,Cart,CartItems,Coupon
from products.models import Product,ProductColorVariant,ProductSizeVariant
import razorpay
from django.conf import settings
# Create your views here.
def login_page(request):
    print(f'request: {request.POST}')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(email=email).first()

        if not user_obj:
            messages.warning(request, 'Account Not Found')
            return redirect(request.path_info)

        

        if not user_obj.profile.is_Email_verified:
            messages.warning(request, 'Your Account Is Not Verified')
            return HttpResponseRedirect(request.path_info)

        authenticated_user = authenticate(username=user_obj.username, password=password)  # Use `username` instead of `email`

        if authenticated_user:
            login(request, authenticated_user)
            return redirect('/')  # Redirect to home after login
        else:
            messages.warning(request, 'Invalid Credentials')
            return redirect(request.path_info)

    return render(request, 'accounts/login.html')


def register_page(request):
    print(f'request:{request.POST}')
    if request.method=="POST":
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj=User.objects.filter(email=email)
        if(user_obj):
           messages.warning(request,'user already exists')
           return HttpResponseRedirect(request.path_info)
        else:
           user_obj=User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
           user_obj.set_password(password)
           user_obj.save()
           print(messages)
           messages.success(request,'A email has been to your mail')
           return HttpResponseRedirect(request.path_info)

    return render(request,'accounts/register.html')

def logout_page(request):
    print(f"Logging out user: {request.user}")  # Debugging to check the user being logged out
    logout(request)  # Django's built-in logout function
    return redirect("/")  # Redirect to home or login page

def profile_page(request):
   user=request.user
   if not user.is_authenticated:
      messages.warning(request,'First Login')
      return render(request,'accounts/login.html')
   else:
      user_obj=User.objects.get(username=user.username)
      profile_obj=Profile.objects.get(user=user_obj)
      context={
         'user':user_obj,
         'profile':profile_obj,
         'cart_count':profile_obj.get_cart_count(),
      }
      return render(request,'accounts/profile.html',context)
      

def cart(request):
   cart=None
   try:
      cart=Cart.objects.get(user=request.user,is_paid=False)
   except Exception as e:
      messages.warning(request,'First Login to see the Items You added Previously')
      return render(request,'accounts/login.html')
   cart_items=CartItems.objects.filter(cart=cart)
   context={
      "cart":cart,
      "cartitems":cart_items,
   }
   if(not cart_items):
      messages.warning(request,f'Add Products to Cart')
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
   if(cart_items):
      client=razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))
      payment=client.order.create({'amount':cart.get_cart_total()*100,'currency':'INR','payment_capture':1})
      cart.razor_pay_order_id=payment['id']
      cart.save()
   
   
   payment=None
   context['payment']=payment
   return render(request,'accounts/cart.html',context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Cart, CartItems, ProductSizeVariant, ProductColorVariant

def add_to_cart(request, uid):
    user = request.user
    product = get_object_or_404(Product, uid=uid)
    
    size = request.GET.get('size')  # Get selected size from request
    color = request.GET.get('color')  # Get selected color from request

    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    size_variant = None
    color_variant = None

    if size:
        size_variant = ProductSizeVariant.objects.filter(product=product, size=size).first()

    if color:
        color_variant = ProductColorVariant.objects.filter(product=product, color=color).first()

    # Check if the product with the same size and color already exists in the cart
    cart_item = CartItems.objects.filter(
        cart=cart, 
        products=product, 
        size_variant=size_variant, 
        color_variant=color_variant
    ).first()

    if cart_item:
        messages.warning(request, "This product is already in your cart with the selected size and color.")
    else:
        cart_item = CartItems.objects.create(
            cart=cart,
            products=product,
            size_variant=size_variant,
            color_variant=color_variant
        )
        messages.success(request, "Product added to cart successfully!")

    return redirect(request.META.get('HTTP_REFERER', 'product:product_list'))  # Redirect back to product page
   
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