from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            total_price = cart.get_total_price()
            order.total_price = total_price
            order.save()
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})

    form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart,
                                                        'form': form})