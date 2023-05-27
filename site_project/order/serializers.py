from rest_framework import serializers

from catalog.serializers import CatalogProductSerializer
from order.models import Order, OrderItem, Payment


class ProductsField(serializers.RelatedField):
    def to_representation(self, value):
        serializer = CatalogProductSerializer(value.product)
        product_data = serializer.data.copy()
        product_data["count"] = value.quantity
        product_data["price"] = value.price
        return product_data


class OrderSerializer(serializers.ModelSerializer):
    products = ProductsField(many=True, read_only=True)
    totalCost = serializers.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        source="get_total_cost",
        read_only=True,
    )
    createdAt = serializers.DateTimeField(format="%d.%m.%y %H:%M", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]

    def create(self, validated_data):
        owner = validated_data.pop("owner")
        cart = validated_data.pop("cart")

        order = Order.objects.create(
            user=owner,
            fullName=owner.fullName,
            email=owner.email,
            phone=owner.phone,
            **validated_data
        )

        for item_data in cart:
            OrderItem.objects.create(order=order, **item_data)

        cart.clear()

        return order


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["number", "name", "month", "year", "code"]

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        return payment
