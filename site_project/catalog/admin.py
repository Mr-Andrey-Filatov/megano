from django.contrib import admin

from catalog.models import (
    CategoryProduct,
    Specifications,
    Tags,
    Product,
    ProductImage,
    Review,
    SaleItem,
)

admin.site.register(CategoryProduct)
admin.site.register(Specifications)
admin.site.register(Tags)
admin.site.register(Review)
admin.site.register(SaleItem)


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "count",
        "price",
        "free_delivery",
        "rating",
        "reviews",
        "date",
        "specifications",
        "category",
        "href",
        "available",
        "limited",
    )

    inlines = [
        ProductImageInline,
    ]
