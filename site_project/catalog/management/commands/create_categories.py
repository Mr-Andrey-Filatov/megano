import os
import random
from pathlib import Path
from typing import Dict

from django.core.files import File
from django.core.management import BaseCommand

from catalog.models import CategoryProduct


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Генерация категорий

        :param args:
        :param options:
        :return:
        """

        self.stdout.write(f"=== Start creating a categories ===")

        categories: Dict = self.data_generation()

        for key, value in categories.items():
            parent_category = None

            if value["parent"] is not None:
                parent_category = CategoryProduct.objects.get(title=value["parent"])

            path = Path(value["image"])

            with path.open(mode="rb") as f:
                category, created = CategoryProduct.objects.get_or_create(
                    title=key, parent=parent_category
                )
                category.image = File(f, name=path.name)
                category.save()

            self.stdout.write(
                "Created category: {title} | href: {href} | image: {image}\n".format(
                    title=category.title,
                    href=category.href(),
                    image=category.image.name,
                )
            )

        self.stdout.write(f"=== End of categories creation ===")

    @staticmethod
    def data_generation() -> Dict:
        """
        Генерация данных для категорий

        :return:
        """

        categories = {}

        categories_names = [
            "Кухонная техника",
            "Микроволновые печи",
            "Мобильные телефоны",
            "Наушники",
            "Скидки!",
            "Стиральные машины",
            "Сумки",
            "Телевизоры",
            "Торшеры",
            "Фотоаппараты",
            "Фурнитура",
            "Чехлы",
        ]

        random.shuffle(categories_names)

        avatars_admin_samples_path = os.path.join(
            os.getcwd(), "frontend/static/frontend/assets/img/icons/departments/"
        )

        photos_samples_names = list(
            map(
                lambda photo_name: os.path.join(avatars_admin_samples_path, photo_name),
                os.listdir(avatars_admin_samples_path),
            )
        )

        random.shuffle(photos_samples_names)

        while len(categories_names) > 0:
            key = random.choice(categories_names)
            image = random.choice(photos_samples_names)

            categories[key] = {"image": image, "parent": None}

            if random.getrandbits(1):
                key_parent = random.choice(list(categories.keys()))

                if (key != key_parent) and (categories[key_parent]["parent"] is None):
                    categories[key]["parent"] = key_parent

            photos_samples_names.remove(image)
            categories_names.remove(key)

        return categories
