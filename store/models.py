from django.db import models
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['sort_order']

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
    slug = models.SlugField(unique=True, blank=True, null=True)
    subtitle = models.CharField(max_length=200)
    description = RichTextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Base price if no sizes specified")
    inventory_stock = models.PositiveIntegerField(default=10, help_text="Base inventory if no sizes specified")
    is_bestseller = models.BooleanField(default=False)
    show_on_home = models.BooleanField(default=True, help_text="Check to display this product on the home page.")
    image_placeholder_tag = models.CharField(max_length=50, choices=IMAGE_CHOICES, default='khlii')

    def __str__(self):
        return f"{self.name} (AED {self.price})"

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size_label = models.CharField(max_length=50, help_text="e.g., 250 ml, 500 ml")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory_stock = models.PositiveIntegerField(default=10)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.product.name} - {self.size_label} (AED {self.price})"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='product_gallery/')
    alt_text = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"

class HeroSlide(models.Model):
    SLIDE_GRAPHICS = [
        ('star', 'Star Emblem'),
        ('jar_red', 'Red Jar (Khlii)'),
        ('pot_gold', 'Gold Pot (Amlou)'),
        ('jar_green', 'Green Jar (Tagine Spice)'),
    ]
    kicker = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.CharField(max_length=200, default="#products-section")
    image = models.ImageField(upload_to='hero_slides/', blank=True, null=True)
    graphic_type = models.CharField(max_length=50, choices=SLIDE_GRAPHICS, default='star')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Slide: {self.title}"

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class SiteContent(models.Model):
    section_key = models.CharField(max_length=100, unique=True, help_text="Type exact key like: about_us")
    title = models.CharField(max_length=200, blank=True, null=True)
    body_text = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='site_images/', blank=True, null=True)

    def __str__(self):
        return f"Content: {self.section_key}"

class CateringInquiry(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    event_date = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Catering Inquiries"

    def __str__(self):
        return f"Catering Inquiry from {self.name} ({self.phone})"

class ContactInquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% off)"
