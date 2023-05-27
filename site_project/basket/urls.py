from django.urls import path

from basket.views import BasketView

urlpatterns = [
    path("api/basket/", BasketView.as_view()),
]
