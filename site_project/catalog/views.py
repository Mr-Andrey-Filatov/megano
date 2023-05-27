from django.db.models import Count
from rest_framework import generics, status, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import BasePagination
from rest_framework.response import Response

from catalog.models import CategoryProduct, Product, Tags, Review, SaleItem
from catalog.serializers import (
    CategoryProductSerializer,
    ProductSerializer,
    TagsSerializer,
    CatalogProductSerializer,
    ReviewSerializer,
    SaleItemSerializer,
)


class CategoriesView(generics.ListAPIView):
    queryset = (
        CategoryProduct.objects.filter(parent=None)
        .prefetch_related("subcategories")
        .order_by()
    )
    serializer_class = CategoryProductSerializer


class CatalogViewPagination(BasePagination):
    def paginate_queryset(self, queryset, request, view=None):
        limit = request.query_params.get("limit")
        return queryset[: int(limit)]

    def get_paginated_response(self, data):
        return Response(
            {
                "items": data,
                "currentPage": 1,
                "lastPage": 30,
            }
        )


class CatalogView(generics.ListAPIView):
    serializer_class = CatalogProductSerializer
    pagination_class = CatalogViewPagination

    def get_queryset(self):
        sort = self.request.query_params.get("sort")
        sortType = self.request.query_params.get("sortType")
        name = self.request.query_params.get("filter[name]")
        min_price = self.request.query_params.get("filter[minPrice]")
        max_price = self.request.query_params.get("filter[maxPrice]")
        free_delivery = self.request.query_params.get("filter[freeDelivery]")
        available = self.request.query_params.get("filter[available]")

        queryset = Product.objects.all()

        if (name is not None) and (name != ""):
            queryset = queryset.filter(title=name)

        if (min_price is not None) and (max_price is not None):
            queryset = queryset.filter(price__gt=min_price, price__lte=max_price)

        if free_delivery:
            queryset = queryset.filter(free_delivery=bool(free_delivery))

        if available:
            queryset = queryset.filter(available=bool(available))

        if (sortType is not None) and (sortType == "dec"):
            sort = "".join(["-", sort])

        queryset = (
            queryset.order_by(sort)
            .select_related("category")
            .prefetch_related("images", "tags")
        )

        return queryset


class ProductsPopularView(generics.ListAPIView):
    queryset = (
        Product.objects.all()
        .annotate(reviews_count=Count("reviews"))
        .order_by("-reviews_count")
        .select_related("category")
        .prefetch_related("images", "tags")[:8]
    )
    serializer_class = CatalogProductSerializer


class ProductsLimitedView(generics.ListAPIView):
    queryset = (
        Product.objects.filter(limited=True)
        .select_related("category")
        .prefetch_related("images", "tags")[:16]
    )
    serializer_class = CatalogProductSerializer


class BannersView(generics.ListAPIView):
    queryset = (
        Product.objects.all()
        .order_by("-rating")
        .select_related("category")
        .prefetch_related("images", "tags")[:3]
    )
    serializer_class = CatalogProductSerializer


class ProductView(RetrieveAPIView):
    queryset = Product.objects.select_related(
        "category", "specifications"
    ).prefetch_related("images", "tags", "reviews")
    serializer_class = ProductSerializer


class ReviewView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwarg):
        serializer_create = self.get_serializer(data=request.data)
        serializer_create.is_valid(raise_exception=True)
        self.perform_create(serializer_create)
        headers = self.get_success_headers(serializer_create.data)

        queryset = Review.objects.filter(product_id=self.kwargs["pk"])
        serializer_list = self.get_serializer(queryset, many=True)
        return Response(
            serializer_list.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TagsView(generics.ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class SaleItemListAPIView(generics.ListAPIView):
    serializer_class = SaleItemSerializer
    queryset = SaleItem.objects.select_related("product").prefetch_related(
        "product__images"
    )
