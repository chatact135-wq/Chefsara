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
    
    related_products = list(Product.objects.filter(category=product.category).exclude(id=product.id)[:3])
    if len(related_products) < 3:
        needed = 3 - len(related_products)
        existing_ids = [product.id] + [p.id for p in related_products]
        fallback_products = list(Product.objects.exclude(id__in=existing_ids).order_by('?')[:needed])
        related_products.extend(fallback_products)

    context = {
        'product': product,
        'categories': categories,
        'promo_dict': promo_dict,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

def category_detail_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all().order_by('sort_order')
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
