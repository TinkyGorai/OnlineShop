from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError
from .models import Product, ProductColorVariant

def product_detail(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)

        # Get the selected color from the request
        selected_color = request.GET.get('color')
        selected_size = request.GET.get('size')

        # Use first available color if none is selected
        if not selected_color and product.product_colors.exists():
            selected_color = product.product_colors.first().color

        # Use first available size if none is selected
        if not selected_size and product.product_sizes.exists():
            selected_size = product.product_sizes.first().size

        # Get price adjustments
        size_variant = product.product_sizes.filter(size=selected_size).first()
        color_variant = product.product_colors.filter(color=selected_color).first()

        final_price = product.base_price
        if size_variant:
            final_price += size_variant.additional_price
        if color_variant:
            final_price += color_variant.additional_price
        color_variants = product.product_colors.values_list('color', flat=True).distinct()
        context = {
            'product': product,
            'selected_color': selected_color,
            'selected_size': selected_size,
            'color_variants':color_variants,
            'size_variants': product.product_sizes.all(),
            'product_images': product.product_colors.filter(color=selected_color),  # Images for selected color
            'final_price': final_price,
        }
        
        return render(request, 'product/product.html', context)

    except Exception as e:
        print(e)
        return HttpResponseServerError("An error occurred")
