from django.db import models
from re import fullmatch

from rest_framework.exceptions import ValidationError

from authapp.models import User
from catalog.models import Product


NOT_INDICATED = "не указано"


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь",
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(
        default=NOT_INDICATED,
        max_length=50,
        verbose_name="ФИО пользователя",
        blank=True,
    )
    email = models.EmailField(
        default=NOT_INDICATED,
        max_length=50,
        verbose_name="email пользователя",
        blank=True,
    )
    phone = models.CharField(
        default=NOT_INDICATED, max_length=30, verbose_name="номер телефона", blank=True
    )
    deliveryType = models.TextField(
        max_length=30, default="ordinary", verbose_name="способ доставки", blank=True
    )
    paymentType = models.TextField(
        max_length=30, default="online", verbose_name="способ оплаты", blank=True
    )
    status = models.TextField(
        max_length=30, default=NOT_INDICATED, verbose_name="статус оплаты", blank=True
    )
    city = models.TextField(
        max_length=30, default=NOT_INDICATED, verbose_name="город доставки", blank=True
    )
    address = models.TextField(
        max_length=30, default=NOT_INDICATED, verbose_name="адрес доставки", blank=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.pk}"

    def get_total_cost(self):
        return sum(product.get_cost() for product in self.products.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="products", verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="Товар",
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return "{}".format(self.pk)

    def get_cost(self):
        return self.price * self.quantity


def validate_year(value):
    if not fullmatch(r"^0[1-9]|[1-9][0-9]$", value):
        raise ValidationError("Year must be between 01 and 99")


def validate_month(value):
    if not fullmatch(r"^0[1-9]|1[0-2]$", value):
        raise ValidationError("Month must be between 01 and 12")


class Payment(models.Model):
    order = models.OneToOneField(
        Order, related_name="payment", on_delete=models.CASCADE, verbose_name="Заказ"
    )
    number = models.IntegerField(default=0, verbose_name="номер счета")
    name = models.TextField(max_length=30, default="не указан")
    month = models.CharField(
        max_length=2, validators=[validate_month], verbose_name="Месяц"
    )
    year = models.CharField(
        max_length=2, validators=[validate_year], verbose_name="Год"
    )
    code = models.IntegerField(default=0, verbose_name="код оплаты")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежы"

    def order_status_change(self):
        self.order.status = "payment"
        self.order.save()

    def __str__(self):
        return self.name
