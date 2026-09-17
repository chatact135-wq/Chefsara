from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Product, PromoCode, HeroSlide, MenuItem, SiteContent, CateringInquiry, ContactInquiry

def home_view(request):
    if request.method == 'POST':
        if 'catering_submit' in request.POST:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            event_date = request.POST.get('event_date')
            if name and phone:
                CateringInquiry.objects.create(name=name, phone=phone, event_date=event_date)
                messages.success(request, 'Catering inquiry submitted successfully!')
            return redirect('/#catering-section')

        elif 'contact_submit' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            if name and email:
                ContactInquiry.objects.create(name=name, email=email, message=message)
                messages.success(request, 'Message sent successfully!')
            return redirect('/#contact-section')

    categories = Category.objects.all()
    products = Product.objects.all()
    slides = HeroSlide.objects.all()
    menu_items = MenuItem.objects.filter(is_active=True)
    site_contents = {sc.section_key: sc for sc in SiteContent.objects.all()}
    promos = PromoCode.objects.filter(is_active=True)
    
    promo_dict = {p.code.upper(): p.discount_percentage for p in promos}

    context = {
        'categories': categories,
        'products': products,
        'slides': slides,
        'menu_items': menu_items,
        'site_contents': site_contents,
        'promo_dict': promo_dict,
    }
    return render(request, 'store/index.html', context)
