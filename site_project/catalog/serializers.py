from rest_framework import serializers
from catalog.models import CategoryProduct, Product, Review, SaleItem


class ImageCategoryField(serializers.Field):
    """Пользовательское поле изображения"""

    def to_representation(self, value):
        image = {"src": value.url, "alt": value.name}

        return image


class SubcategoriesField(serializers.RelatedField):
    """Пользовательское поле отношений подкатегорий"""

    def to_representation(self, value):
        subcategories = {
            "id": value.id,
            "title": value.title,
            "image": {"src": value.image.url, "alt": value.image.name},
            "href": value.href(),
        }

        return subcategories


class CategoryProductSerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    image = ImageCategoryField()
    subcategories = SubcategoriesField(many=True, read_only=True)

    class Meta:
        model = CategoryProduct
        fields = ["id", "title", "image", "href", "subcategories"]


class ReviewsField(serializers.RelatedField):
    """Пользовательское поле отношений отзывов"""

    def to_representation(self, value):
        reviews = {
            "author": value.author,
            "email": value.email,
            "text": value.text,
            "rate": value.rate,
            "date": value.date,
        }

        return reviews


class SpecificationsField(serializers.RelatedField):
    """Пользовательское поле отношений характеристик"""

    def to_representation(self, value):
        specifications = [{"name": value.name, "value": value.value}]

        return specifications


class CatalogProductSerializer(serializers.Serializer):
    """Сериализатор продукт каталога"""

    id = serializers.IntegerField()
    category = serializers.CharField(source="category.title")
    price = serializers.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = serializers.IntegerField()
    date = serializers.DateField()
    title = serializers.CharField()
    description = serializers.CharField()
    href = serializers.CharField()
    free_delivery = serializers.BooleanField()
    images = serializers.StringRelatedField(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    reviews = serializers.IntegerField(source="get_reviews_count", read_only=True)
    rating = serializers.IntegerField()


class ProductSerializer(CatalogProductSerializer):
    """Сериализатор деталий продукта"""

    reviews = ReviewsField(many=True, read_only=True)
    specifications = SpecificationsField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзыва"""

    class Meta:
        model = Review
        fields = ["author", "email", "text", "rate", "date"]
        read_only_fields = ["date"]

    def validate(self, data):
        user = self.context["request"].user

        if (user.fullName != data["author"]) or (user.email != data["email"]):
            raise serializers.ValidationError(
                "The name or email you entered does not match your account information"
            )

        return data

    def create(self, validated_data):
        pk = self.context["view"].kwargs["pk"]
        product = Product.objects.get(pk=pk)
        review, created = Review.objects.get_or_create(
            **validated_data,
            product=product,
        )
        return review


class TagsIdField(serializers.Field):
    """Пользовательское поле идентификатора тегоа"""

    def to_representation(self, value):
        str_id = value.lower()

        return str_id


class TagsSerializer(serializers.Serializer):
    """Сериализатор деталий продукта"""

    id = TagsIdField(source="name")
    name = serializers.CharField()


class SaleItemSerializer(serializers.ModelSerializer):
    price = serializers.CharField(source="product.price")
    title = serializers.CharField(source="product.title")
    images = serializers.StringRelatedField(
        source="product.images", many=True, read_only=True
    )

    class Meta:
        model = SaleItem
        fields = (
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "href",
            "images",
        )
