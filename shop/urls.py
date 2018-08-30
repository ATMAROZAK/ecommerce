from django.urls import path
from . import views

urlpatterns = [
    path('<slug:category_slug>/', views.ProductList, name='ProductListByCategory'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', views.ProductList, name='ProductListBySubcategory'),
    path('product/<slug:brand_slug>/<slug:slug>/', views.ProductDetail, name='ProductDetail'),
    path('', views.ProductList, name='ProductList'),
]