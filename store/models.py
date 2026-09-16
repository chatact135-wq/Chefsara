from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    IMAGE_CHOICES = [
        ('khlii', 'Moroccan Khlii Jar (Maroon Confit)'),
        ('smen', 'Moroccan Smen Pot (Cultured Butter)'),
        ('lemon', 'Preserved Lemon Jar (Salt-Cured)'),
        ('orange_jam', 'Moroccan Orange Jam (Bright Orange)'),
        ('lemon_jam', 'Moroccan Lemon Jam (Light Citrus)'),
        ('spice_ras', 'Ras el Hanout Spice Jar (Deep Red)'),
        ('spice_tagine', 'Tagine Spice Blend Jar (Deep Green)'),
        ('spice_chermoula', 'Chermoula Spice Jar (Golden Mustard)'),
        ('spice_couscous', 'Couscous Spice Jar (Warm Brown)'),
        ('amlou_orig', 'Amlou Original Pot (Amber Honey)'),
        ('amlou_dxb', 'Amlou DXB Style Pot (Rich Cocoa)'),
        ('amlou_dates', 'Amlou Dates & Nuts Pot (Deep Rust)'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory_stock = models.PositiveIntegerField(default=10)
    is_bestseller = models.BooleanField(default=False)
    image_placeholder_tag = models.CharField(
        max_length=50, 
        choices=IMAGE_CHOICES, 
        default='khlii'
    )

    def __str__(self):
        return f"{self.name} (AED {self.price})"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.PositiveIntegerField(help_text="Enter discount percentage e.g. 10 for 10%")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% off)"
