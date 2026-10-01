import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, HeroSlide, MenuItem, SiteContent, PromoCode, CateringInquiry, ContactInquiry, ShippingRate, Order

# --- ZIINA API KEY ---
ZIINA_API_KEY = os.environ.get('ZIINA_API_KEY', 'O9Uf/VlL49DsIarGi1UzZA2IwqSEcYNa2EtECMNcJuyjAcSNtY/19FvToVb6831H')

def get_smart_shipping_dict():
    shipping_rates = ShippingRate.objects.filter(is_active=True)
    rates_list = []
    for sr in shipping_rates:
        keys = []
        if sr.location_name:
            keys.extend([k.strip().lower() for k in sr.location_name.split(',')])
        if sr.location_name_ar:
            keys.extend([k.strip().lower() for k in sr.location_name_ar.split(',')])
        rates_list.append({
            'fee': float(sr.shipping_fee),
            'keywords': [k for k in keys if k]
        })
    return json.dumps(rates_list)

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
        'shipping_dict': get_smart_shipping_dict(),
        'default_shipping': 25.00,
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
        'shipping_dict': get_smart_shipping_dict(),
        'default_shipping': 25.00,
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
        'shipping_dict': get_smart_shipping_dict(),
        'default_shipping': 25.00,
    }
    return render(request, 'store/category_detail.html', context)


# ==========================================
# ZIINA PAYMENT INTEGRATION & ORDER TRACKING
# ==========================================
@csrf_exempt
def process_ziina_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total_amount = float(data.get('total_amount', 0))
            amount_in_fils = int(total_amount * 100)

            # 1. Store the Order Details to the Database FIRST
            cart_items = data.get('cart_items', [])
            cart_text = "\n".join([f"{item['quantity']}x {item['name']} (AED {item['price']})" for item in cart_items])
            
            new_order = Order.objects.create(
                customer_name=data.get('customer_name', 'Unknown'),
                customer_phone=data.get('customer_phone', 'Unknown'),
                customer_address=data.get('customer_address', 'Unknown'),
                cart_summary=cart_text,
                total_amount=total_amount,
                is_paid=False
            )

            # 2. Tell Ziina to process the payment and return the Order ID if successful
            url = "https://api-v2.ziina.com/api/payment_intent"
            payload = {
                "amount": amount_in_fils,
                "currency_code": "AED",
                "message": f"Order from BY CHEF SARA - {new_order.customer_name}",
                "success_url": request.build_absolute_uri(f'/payment-success/?ref={new_order.order_id}'),
                "cancel_url": request.build_absolute_uri('/payment-failure/'),
                "failure_url": request.build_absolute_uri('/payment-failure/'),
                "test": True  
            }
            headers = {
                "Authorization": f"Bearer {ZIINA_API_KEY}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            try:
                response_data = response.json()
                if 'redirect_url' in response_data:
                    return JsonResponse({'success': True, 'redirect_url': response_data['redirect_url']})
                else:
                    return JsonResponse({'success': False, 'error': response.text})
            except Exception:
                return JsonResponse({'success': False, 'error': response.text})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid Request'})

def payment_success(request):
    # If the payment succeeds, grab the secure reference ID and mark it as Paid!
    ref = request.GET.get('ref')
    if ref:
        try:
            order = Order.objects.get(order_id=ref)
            order.is_paid = True
            order.save()
        except Exception:
            pass

    return render(request, 'store/success.html', {'message': 'Thank you! Your payment was successful and your order is confirmed.'})

def payment_failure(request):
    return render(request, 'store/failure.html', {'message': 'Your payment was cancelled or failed. Please try again.'})
