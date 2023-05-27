from django.contrib import admin

from order.models import Order, OrderItem, Payment


admin.site.register(Payment)


class OrderItemInline(admin.StackedInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "createdAt",
        "fullName",
        "email",
        "phone",
        "deliveryType",
        "paymentType",
        "get_total_cost",
        "status",
        "city",
        "address",
    )

    inlines = [
        OrderItemInline,
    ]
