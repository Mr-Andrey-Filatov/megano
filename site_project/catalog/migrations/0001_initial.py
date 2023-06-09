# Generated by Django 4.2 on 2023-05-18 20:28

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CategoryProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=50, verbose_name="название категории"),
                ),
                (
                    "image",
                    models.FileField(
                        null=True,
                        upload_to=catalog.models.category_image_directory_path,
                        validators=[catalog.models.CategoryProduct.validate_image],
                        verbose_name="иконка",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subcategories",
                        to="catalog.categoryproduct",
                        verbose_name="подкатегории",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=50, verbose_name="название товара"),
                ),
                (
                    "description",
                    models.TextField(max_length=100, verbose_name="описание товара"),
                ),
                (
                    "count",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="количество "
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=8,
                        verbose_name="цена товара",
                    ),
                ),
                ("free_delivery", models.BooleanField(default=True)),
                (
                    "rating",
                    models.PositiveIntegerField(
                        default=0, verbose_name="счетчик покупок данного товара"
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "available",
                    models.BooleanField(default=True, verbose_name="в наличии"),
                ),
                (
                    "limited",
                    models.BooleanField(
                        default=False, verbose_name="ограниченый тираж"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.categoryproduct",
                        verbose_name="категория товара",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
        migrations.CreateModel(
            name="Specifications",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="название")),
                ("value", models.CharField(max_length=50, verbose_name="значение")),
            ],
            options={
                "verbose_name": "Спецификация",
                "verbose_name_plural": "Спецификации",
            },
        ),
        migrations.CreateModel(
            name="Tags",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="тэг товара")),
            ],
            options={
                "verbose_name": "Тэг",
                "verbose_name_plural": "Тэги",
            },
        ),
        migrations.CreateModel(
            name="SaleItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "salePrice",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=8,
                        verbose_name="Сниженная цена",
                    ),
                ),
                ("dateFrom", models.DateField(verbose_name="От дата")),
                ("dateTo", models.DateField(verbose_name="До даты")),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_items",
                        to="catalog.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Распродажа",
                "verbose_name_plural": "Распродажи",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "author",
                    models.CharField(max_length=100, verbose_name="пользователь"),
                ),
                (
                    "email",
                    models.EmailField(max_length=100, verbose_name="электроная почта"),
                ),
                ("text", models.CharField(max_length=100, verbose_name="текст отзыва")),
                ("rate", models.PositiveSmallIntegerField()),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="catalog.product",
                        verbose_name="товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=catalog.models.product_images_directory_path,
                        verbose_name="image",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="catalog.product",
                        verbose_name="изображения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение продукта",
                "verbose_name_plural": "изображения продуктов",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="specifications",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.specifications",
                verbose_name="спецификация товара",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="tags",
            field=models.ManyToManyField(related_name="tags", to="catalog.tags"),
        ),
    ]
