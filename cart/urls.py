from django.urls import path
from . import views
urlpatterns = [
    path('remove/<int:product_id>/', views.CartRemove, name='CartRemove'),
    path('add/<int:product_id>/', views.CartAdd, name='CartAdd'),
    path('', views.CartDetail, name='CartDetail'),
]