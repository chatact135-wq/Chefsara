from django.shortcuts import render
from .models import Category, Product

def home_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/index.html', context)
