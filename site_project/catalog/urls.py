from django.urls import path

from catalog.views import (
    CategoriesView,
    CatalogView,
    ProductsPopularView,
    ProductsLimitedView,
    BannersView,
    ProductView,
    TagsView,
    ReviewView,
    SaleItemListAPIView,
)

urlpatterns = [
    path("api/banners/", BannersView.as_view()),
    path("api/products/popular/", ProductsPopularView.as_view()),
    path("api/products/limited/", ProductsLimitedView.as_view()),
    path("api/categories/", CategoriesView.as_view()),
    path("api/catalog/", CatalogView.as_view()),
    path("api/catalog/<int:pk>/", CatalogView.as_view()),
    path("api/products/<int:pk>", ProductView.as_view()),
    path("api/product/<int:pk>/review", ReviewView.as_view()),
    path("api/sales/", SaleItemListAPIView.as_view()),
    path("api/tags", TagsView.as_view()),
]
