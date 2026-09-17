from django.contrib import admin
from .models import Category, Product, PromoCode, HeroSlide, MenuItem, SiteContent, CateringInquiry, ContactInquiry

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'sort_order')
    list_editable = ('sort_order',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'inventory_stock', 'is_bestseller')
    list_filter = ('category', 'is_bestseller')
    search_fields = ('name', 'description')

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
