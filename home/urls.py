from django.contrib import admin
from django.urls import path
from .views import index,Product_list,product_search
urlpatterns = [
   path('',index,name="index"),
   path('search/',product_search,name="product_search"),
   path('<slug:category_slug>/',Product_list,name="Product_list"),
]
