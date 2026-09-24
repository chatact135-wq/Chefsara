from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from store.sitemaps import StaticViewSitemap, CategorySitemap, ProductSitemap
from store import views  # Corrected import from the store app

sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('product/<slug:product_slug>/', views.product_detail_view, name='product_detail'),
    path('category/<slug:category_slug>/', views.category_detail_view, name='category_detail'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
