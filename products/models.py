from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

class Category(BaseModel): 
    category_name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class Product(BaseModel):
    product_name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    base_price = models.IntegerField()  # Base price without size/color addition
    product_description = models.TextField()
    brand = models.CharField(max_length=100, blank=True)
    fabric = models.CharField(max_length=100, blank=True)
    rating = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_price_for_size_and_color(self, size=None, color=None):
        """
        Returns the final price based on size and color variant price addition.
        """
        final_price = self.base_price

        size_variant = self.product_sizes.filter(size=size).first()
        if size_variant:
            final_price += size_variant.additional_price

        color_variant = self.product_colors.filter(color=color).first()
        if color_variant:
            final_price += color_variant.additional_price

        return final_price

class ProductSizeVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_sizes")
    size = models.CharField(max_length=50)
    additional_price = models.IntegerField(default=0)  # Extra charge for this size

    def __str__(self):
        return f"{self.product.product_name} - {self.size} (+{self.additional_price})"


class ProductColorVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_colors")
    color = models.CharField(max_length=50)
    additional_price = models.IntegerField(default=0)  # Extra charge for this color
    image = models.ImageField(upload_to="product")

    def __str__(self):
        return f"{self.product.product_name} - {self.color} (+{self.additional_price})"


