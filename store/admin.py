from django.contrib import admin
from .models import Category, Product, PromoCode, HeroSlide

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'inventory_stock', 'is_bestseller')
    list_filter = ('category', 'is_bestseller')
    search_fields = ('name', 'description')

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'kicker', 'order')
    list_editable = ('order',)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)
