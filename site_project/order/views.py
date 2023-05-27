from rest_framework import permissions, status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
    GenericAPIView,
    ListAPIView,
)
from rest_framework.response import Response

from basket.cart import Cart
from order.models import Order
from order.serializers import OrderSerializer, PaymentSerializer


class HistoryOrderView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        orders = Order.objects.filter(user_id=self.request.user.pk)
        return orders


class CreateOrderView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, cart=Cart(self.request))

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        response.data = {"response": "Successful order confirmed"}
        return response


class PaymentView(CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        order = get_object_or_404(Order, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save(order=order)
        payment.order_status_change()

        return Response(
            {"response": "Successfully payment"}, status=status.HTTP_201_CREATED
        )


class ActiveOrderView(GenericAPIView):
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        order = Order.objects.order_by("-createdAt").first()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
