from django.shortcuts import render
from .models import Category, Product, PromoCode

def home_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    promos = PromoCode.objects.filter(is_active=True)
    
    # Convert promos into a dictionary for easy JS lookup e.g. {'SARA10': 10}
    promo_dict = {p.code.upper(): p.discount_percentage for p in promos}

    context = {
        'categories': categories,
        'products': products,
        'promo_dict': promo_dict,
    }
    return render(request, 'store/index.html', context)
