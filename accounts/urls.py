from django.contrib import admin
from django.urls import path
from .views import login_page,register_page,add_to_cart,cart,remove_from_cart,remove_coupon,success,logout_page,profile_page,create_order,modified_cart
urlpatterns = [
    path('login/', login_page,name="login"),
    path('register/', register_page,name="register"),
    path('logout/', logout_page,name="logout"),
    path('profile/', profile_page,name="profile"),
    path('cart/',cart,name="cart"),
    path('add-to-cart/<uid>/',add_to_cart,name="add_to_cart"),
    path('remove-from-cart/<cart_item_uid>/',remove_from_cart,name="remove_from_cart"),
    path('remove-coupon/<cart_item_uid>/',remove_coupon,name="remove-coupon"),
    path('success/',success,name="success"),
    path('order/',create_order,name="order"),
    path('modified_cart/<uuid:item_id>/<str:action>/',modified_cart,name="modified_cart"),
]
