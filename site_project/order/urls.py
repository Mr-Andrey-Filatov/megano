from django.urls import path

from order.views import (
    CreateOrderView,
    OrderView,
    PaymentView,
    ActiveOrderView,
    HistoryOrderView,
)

urlpatterns = [
    path("api/history-orders/", HistoryOrderView.as_view()),
    path("api/orders/", CreateOrderView.as_view()),
    path("api/orders/<int:pk>", OrderView.as_view()),
    path("api/orders/<int:pk>/", OrderView.as_view()),
    path("api/payment/<int:pk>/", PaymentView.as_view()),
    path("api/orders/active/", ActiveOrderView.as_view()),
]
