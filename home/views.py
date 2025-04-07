from django.shortcuts import render, get_object_or_404
from products.models import Product, Category, ProductSizeVariant, ProductColorVariant
from django.http import HttpResponseServerError
from django.shortcuts import render, get_object_or_404
# Create your views here.
def index(request):
    category=Category.objects.all()
    context={"category":category}
    return render(request,'home/index.html',context)

def Product_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    # Fetch products in the selected category
    products = Product.objects.filter(category=category)

    # Extract filters from request.GET
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_brand = request.GET.get('brand', '')
    selected_fabric = request.GET.get('fabric', '')
    selected_sizes = request.GET.getlist('size')
    selected_rating = request.GET.get('rating')
    availability = request.GET.get('available')

    # Apply filters
    if min_price:
        products = products.filter(base_price__gte=int(min_price))
    if max_price:
        products = products.filter(base_price__lte=int(max_price))
    if selected_brand:
        products = products.filter(brand=selected_brand)
    if selected_fabric:
        products = products.filter(fabric=selected_fabric)
    if selected_rating:
        products = products.filter(Rating__gte=int(selected_rating))  # Filter by min rating
    if availability == "on":
        products = products.filter(Availability=True)

    # Prepare context for template
    context = {
        'category': category,
        'products': products,  # Pass the filtered products
        'brands': Product.objects.values_list('brand', flat=True).distinct(),
        'fabrics': Product.objects.values_list('fabric', flat=True).distinct(),
        'size_variants': ProductSizeVariant.objects.all(),
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'selected_brand': selected_brand,
        'selected_fabric': selected_fabric,
        'selected_rating': selected_rating,
        'availability': availability,
    }
    return render(request, 'product/productlist.html', context)

def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(product_name__icontains=query)
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'product/product_search.html', context)  
