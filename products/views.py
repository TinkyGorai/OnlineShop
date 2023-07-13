from django.shortcuts import render
from .models import Product
from django.http import HttpResponseServerError
# Create your views here.
def product_detail(request,slug):
    try:
      product=Product.objects.get(slug=slug)
      context={'product':product}
      if request.GET.get('size'):
        size=request.GET.get('size')
        price=product.product_price_by_size(size)
        print(price)
        context['select_size']=size
        context['updated_price']=price
      return render(request,'product/product.html',context)

    except Exception as e:
        print(e)
        return HttpResponseServerError("An error occurred")