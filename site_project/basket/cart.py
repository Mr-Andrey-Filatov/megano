from decimal import Decimal
from django.conf import settings
from catalog.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def change_quantity(self, product, quantity):
        pk_str = str(product.pk)

        if (pk_str not in self.cart) and (quantity > 0):
            self.cart[pk_str] = {
                "quantity": quantity if quantity <= product.count else product.count,
                "price": str(product.price),
            }
        else:
            pre_quantity = self.cart[pk_str]["quantity"] + quantity

            if pre_quantity > product.count:
                self.cart[pk_str]["quantity"] = product.count
            else:
                self.cart[pk_str]["quantity"] += quantity

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            return self.save()

    def get_all_products(self):
        product_ids = self.cart.keys()

        products = (
            Product.objects.filter(id__in=product_ids)
            .select_related("category")
            .prefetch_related("images", "tags")
        )

        for product in products:
            product.count = self.cart.get(str(product.pk)).get("quantity")
            product.price = self.cart.get(str(product.pk)).get("price")

        return products

    def __iter__(self):
        for key, value in self.cart.items():
            yield dict(product_id=key, **value)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
