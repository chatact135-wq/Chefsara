from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<slug:product_slug>/', views.product_detail_view, name='product_detail'),
    path('category/<slug:category_slug>/', views.category_detail_view, name='category_detail'),
]
