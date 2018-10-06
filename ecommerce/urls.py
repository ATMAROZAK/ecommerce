from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from shop.views import payeer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/',include(('cart.urls', 'cart'), namespace='cart')),
    path('order/',include(('orders.urls', 'orders'), namespace='orders')),
    path('payeer_656214683.txt/', payeer),
    path('', include(('shop.urls', 'shop'), namespace='shop')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

