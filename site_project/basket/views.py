from django.http import HttpRequest
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from basket.cart import Cart
from catalog.models import Product
from catalog.serializers import CatalogProductSerializer


class BasketView(generics.ListAPIView):
    serializer_class = CatalogProductSerializer

    def get_queryset(self):
        product = None
        request: HttpRequest = self.request
        cart = Cart(self.request)

        pk = request.data.get("id") or self.request.query_params.get("id")
        quantity = request.data.get("count")

        if pk:
            product = get_object_or_404(Product, pk=pk)

        if (request.method == "POST") and quantity:
            cart.change_quantity(product=product, quantity=quantity)
        elif request.method == "DELETE":
            cart.remove(product)

        queryset = cart.get_all_products()

        return queryset

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
