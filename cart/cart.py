from decimal import Decimal
from django.conf import settings
from shop.models import Product
from .models import Shipping


class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        print('Cart: ' + str(self.cart))


    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def remove_shipping(self):

        del self.cart['shipping']
        self.save()

    # Итерация по товарам
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():

            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # Количество товаров
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True



class ShippingCart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        shipping_cart = self.session.get(settings.SHIPPING_CART_SESSION_ID)
        if not shipping_cart:
            # Сохраняем корзину пользователя в сессию
            shipping_cart = self.session[settings.SHIPPING_CART_SESSION_ID] = {}
        self.shipping_cart = shipping_cart

        #self.add(Shipping.objects.get(defaullt=True))
        print("ship :"  + str(self.shipping_cart))

    def add(self, shipping, update=False):
        shipping_id = str(shipping.id)

        if update:
            self.remove()

        if shipping_id not in self.shipping_cart:
            self.shipping_cart[shipping_id] = {'price': str(shipping.price)}

        self.save()

    def remove(self):
        keys = list(self.shipping_cart.keys())
        for key in keys:
            del self.shipping_cart[key]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.shipping_cart
        # Указываем, что сессия изменена
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.shipping_cart.values())

    def __iter__(self):
        shipping_ids = self.shipping_cart.keys()
        shippings = Shipping.objects.filter(id__in=shipping_ids)

        for shipping in shippings:
            self.shipping_cart[str(shipping.id)]['shipping'] = shipping

        for item in self.shipping_cart.values():
            item['price'] = Decimal(item['price'])
            yield item