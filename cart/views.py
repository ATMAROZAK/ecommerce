from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from shop.models import Product
from .models import Shipping
from .cart import Cart
from .shipping import ShippingCart
from .forms import CartAddProductForm, ShippingForm


@require_POST
def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                                  update_quantity=cd['update'])
    return redirect('cart:CartDetail')


@require_POST
def ShippingAdd(request):
    shipping_cart = ShippingCart(request)
    #shipping = get_object_or_404(Shipping, id=shipping_id)
    form = ShippingForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        shipping_cart.add_shipping(shipping=cd['shipping'], update=True)
    return redirect('cart:CartDetail')


def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')


def RemoveShipping(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:CartDetail')


def CartDetail(request):
    cart = Cart(request)
    shipping_cart = ShippingCart(request)

    total_price = cart.get_total_price() + shipping_cart.get_total_price()

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })

    shipping_form = ShippingForm(initial={
                'shipping' : Shipping.objects.get(id=shipping_cart.shipping_cart['shipping']['id'])
            })
    print(cart.cart)
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'shipping_cart': shipping_cart,
                                                'shipping_form': shipping_form,
                                                'total_price' : total_price})