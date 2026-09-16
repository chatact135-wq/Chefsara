from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory_stock = models.PositiveIntegerField(default=10)
    is_bestseller = models.BooleanField(default=False)
    image_placeholder_tag = models.CharField(max_length=100, default="[ Jar SVG ]")

    def __str__(self):
        return f"{self.name} (AED {self.price})"
