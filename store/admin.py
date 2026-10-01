from django.contrib import admin
from .models import Category, Product, ProductSize, ProductImage, PromoCode, HeroSlide, MenuItem, SiteContent, CateringInquiry, ContactInquiry, ShippingRate, Order

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 2

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'sort_order')
    list_editable = ('sort_order',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_bestseller')
    list_filter = ('category', 'is_bestseller')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline, ProductImageInline]

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'kicker', 'order')
    list_editable = ('order',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('section_key', 'title')
    search_fields = ('section_key', 'title')

@admin.register(CateringInquiry)
class CateringInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'event_date', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('name', 'phone')
    ordering = ('-created_at',)

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at',)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)

@admin.register(ShippingRate)
class ShippingRateAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'shipping_fee', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('location_name', 'location_name_ar')
    list_editable = ('shipping_fee', 'is_active')

# --- NEW ORDER ADMIN ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_phone', 'total_amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_address')
    readonly_fields = ('order_id', 'created_at', 'cart_summary')
    list_editable = ('is_paid',)  # Lets you manually toggle "Paid" from the main list just in case!
