from decimal import Decimal
from django.conf import settings
from .models import Shipping

class ShippingCart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        shipping_cart = self.session.get(settings.SHIPPING_CART_SESSION_ID)
        if not shipping_cart:
            # Сохраняем корзину пользователя в сессию
            shipping_cart = self.session[settings.SHIPPING_CART_SESSION_ID] = {}
        self.shipping_cart = shipping_cart


        if list(self.shipping_cart.values()) == []:
            self.add_shipping(Shipping.objects.get(defaullt=True))

        print("ship :"  + str(self.shipping_cart))

    def add_shipping(self, shipping, update=False):

        if update:
            self.remove()

        if 'shipping' not in self.shipping_cart:
            self.shipping_cart['shipping'] = {'price': str(shipping.price),
                                              'quantity' : 0}
        self.save()

    def remove(self):
        keys = list(self.shipping_cart.keys())
        for key in keys:
            del self.shipping_cart[key]
            self.save()

    def save(self):
        self.session[settings.SHIPPING_CART_SESSION_ID] = self.shipping_cart
        # Указываем, что сессия изменена
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.shipping_cart.values())

    def __iter__(self):

        for item in self.shipping_cart.values():
            item['price'] = Decimal(item['price'])
            yield item