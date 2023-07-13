from django.shortcuts import render
from products.models import Product
# Create your views here.
def index(request):
    product=Product.objects.all()
    context={"product":product}
    return render(request,'home/index.html',context)