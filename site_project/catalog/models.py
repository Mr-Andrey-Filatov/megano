from django.core.exceptions import ValidationError
from django.db import models

from authapp.models import User


def category_image_directory_path(instance: "CategoryProduct", filename: str) -> str:
    return "categories/category_{pk}/image/{filename}".format(
        pk=instance.pk, filename=filename
    )


class CategoryProduct(models.Model):
    def validate_image(fieldfile_obj):
        file_size = fieldfile_obj.size
        megabyte_limit = 150.0
        if file_size > megabyte_limit * 1024 * 1024:
            raise ValidationError(
                "Максимальный размер файла {}MB".format(str(megabyte_limit))
            )

    title = models.CharField(max_length=50, verbose_name="название категории")
    image = models.FileField(
        upload_to=category_image_directory_path,
        null=True,
        validators=[validate_image],
        verbose_name="иконка",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
        db_index=True,
        verbose_name="подкатегории",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def href(self):
        return f"/catalog/{self.pk}"

    def __str__(self):
        return self.title


class Specifications(models.Model):
    name = models.CharField(max_length=50, verbose_name="название")
    value = models.CharField(max_length=50, verbose_name="значение")

    class Meta:
        verbose_name = "Спецификация"
        verbose_name_plural = "Спецификации"

    def __str__(self):
        return f"{self.name} | {self.value}"


class Tags(models.Model):
    name = models.CharField(max_length=50, verbose_name="тэг товара")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name="название товара")
    description = models.TextField(max_length=100, verbose_name="описание товара")
    count = models.PositiveSmallIntegerField(default=0, verbose_name="количество ")
    price = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, verbose_name="цена товара"
    )
    free_delivery = models.BooleanField(default=True)
    rating = models.PositiveIntegerField(
        default=0, verbose_name="счетчик покупок данного товара"
    )
    date = models.DateField(auto_now_add=True)
    specifications = models.ForeignKey(
        Specifications, on_delete=models.CASCADE, verbose_name="спецификация товара"
    )
    category = models.ForeignKey(
        CategoryProduct, on_delete=models.CASCADE, verbose_name="категория товара"
    )
    tags = models.ManyToManyField(Tags, related_name="tags")
    available = models.BooleanField(default=True, verbose_name="в наличии")
    limited = models.BooleanField(default=False, verbose_name="ограниченый тираж")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def href(self):
        return f"/product/{self.pk}"

    def get_reviews_count(self):
        return self.reviews.count()

    def __str__(self):
        return self.title


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk, filename=filename
    )


class ProductImage(models.Model):
    class Meta:
        verbose_name_plural = "изображения продуктов"
        verbose_name = "Изображение продукта"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="изображения",
    )
    image = models.ImageField(
        upload_to=product_images_directory_path, verbose_name="image"
    )

    def __str__(self):
        return self.image.url


class Review(models.Model):
    author = models.CharField(max_length=100, verbose_name="пользователь")
    email = models.EmailField(max_length=100, verbose_name="электроная почта")
    text = models.CharField(max_length=100, verbose_name="текст отзыва")
    rate = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="товар", related_name="reviews"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.text


class SaleItem(models.Model):
    salePrice = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, verbose_name="Сниженная цена"
    )
    dateFrom = models.DateField(verbose_name="От дата")
    dateTo = models.DateField(verbose_name="До даты")
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="sale_items",
        verbose_name="Товар",
    )

    class Meta:
        verbose_name = "Распродажа"
        verbose_name_plural = "Распродажи"

    def href(self):
        return f"/product/{self.product.pk}"

    def __str__(self):
        return f'Распродажа "{self.product.title}"'
