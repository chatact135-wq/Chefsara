from django.shortcuts import render
from .models import Category, Product, PromoCode, HeroSlide

def home_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    slides = HeroSlide.objects.all()
    promos = PromoCode.objects.filter(is_active=True)
    
    promo_dict = {p.code.upper(): p.discount_percentage for p in promos}

    context = {
        'categories': categories,
        'products': products,
        'slides': slides,
        'promo_dict': promo_dict,
    }
    return render(request, 'store/index.html', context)
