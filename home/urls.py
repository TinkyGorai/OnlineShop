from django.contrib import admin
from django.urls import path
from .views import index,Product_list
urlpatterns = [
   path('',index,name="index"),
   path('<slug:category_slug>/',Product_list,name="Product_list"),
]
