from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, HeroSlide, MenuItem, SiteContent, PromoCode, CateringInquiry, ContactInquiry

def home_view(request):
    if request.method == 'POST':
        if 'catering_submit' in request.POST:
            CateringInquiry.objects.create(
                name=request.POST.get('name'),
                phone=request.POST.get('phone'),
                event_date=request.POST.get('event_date')
            )
            return redirect('home')
        elif 'contact_submit' in request.POST:
            ContactInquiry.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                message=request.POST.get('message')
            )
            return redirect('home')

    slides = HeroSlide.objects.all()
    categories = Category.objects.all().order_by('sort_order')
    
    # Only show products on the home page if 'show_on_home' is checked True in the admin
    products = Product.objects.filter(show_on_home=True)
    
    promo_codes = PromoCode.objects.filter(is_active=True)
    promo_dict = {p.code.upper(): p.discount_percentage for p in promo_codes}

    context = {
        'slides': slides,
        'categories': categories,
        'products': products,
        'promo_dict': promo_dict,
    }
    return render(request, 'store/index.html', context)

def product_detail_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    categories = Category.objects.all().order_by('sort_order')
    promo_codes = PromoCode.objects.filter(is_active=True)
    promo_dict = {p.code.upper(): p.discount_percentage for p in promo_codes}
    
    context = {
        'product': product,
        'categories': categories,
        'promo_dict': promo_dict,
    }
    return render(request, 'store/product_detail.html', context)

def category_detail_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all().order_by('sort_order')
    
    # Category pages show all products belonging to this category regardless of the home flag
    products = category.products.all()
    
    promo_codes = PromoCode.objects.filter(is_active=True)
    promo_dict = {p.code.upper(): p.discount_percentage for p in promo_codes}

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'promo_dict': promo_dict,
    }
    return render(request, 'store/category_detail.html', context)
