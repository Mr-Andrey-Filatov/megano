from django.urls import path
from django.views.generic import TemplateView
from rest_framework.urls import app_name

urlpatterns = [
    path("", TemplateView.as_view(template_name="frontend/index.html")),
    path("login/", TemplateView.as_view(template_name="frontend/login.html")),
    path("about/", TemplateView.as_view(template_name="frontend/about.html")),
    path("account/", TemplateView.as_view(template_name="frontend/account.html")),
    path("cart/", TemplateView.as_view(template_name="frontend/cart.html")),
    path("catalog/", TemplateView.as_view(template_name="frontend/catalog.html")),
    path(
        "catalog/<int:pk>", TemplateView.as_view(template_name="frontend/catalog.html")
    ),
    path(
        "history-order/",
        TemplateView.as_view(template_name="frontend/historyorder.html"),
    ),
    path(
        "order-detail/<int:pk>",
        TemplateView.as_view(template_name="frontend/oneorder.html"),
    ),
    path("order/<int:pk>", TemplateView.as_view(template_name="frontend/order.html")),
    path(
        "payment/<int:pk>", TemplateView.as_view(template_name="frontend/payment.html")
    ),
    path(
        "payment-someone/",
        TemplateView.as_view(template_name="frontend/paymentsomeone.html"),
    ),
    path(
        "product/<int:pk>", TemplateView.as_view(template_name="frontend/product.html")
    ),
    path("profile/", TemplateView.as_view(template_name="frontend/profile.html")),
    path(
        "progress-payment/",
        TemplateView.as_view(template_name="frontend/progressPayment.html"),
    ),
    path("sale/", TemplateView.as_view(template_name="frontend/sale.html")),
]
