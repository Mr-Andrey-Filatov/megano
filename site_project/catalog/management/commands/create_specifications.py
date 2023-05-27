from django.core.management import BaseCommand

from catalog.models import Specifications


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Генерация характеристик

        :param args:
        :param options:
        :return:
        """

        self.stdout.write(f"=== Start creating a specifications ===")

        specifications_title = [
            "Телевизор",
            "Наушники",
            "Стиральная машина",
            "Аксессуар",
            "Чехол",
            "Электроника",
            "Фотоаппарат",
            "Фурнитура",
            "Мобильный телефон",
            "Сумка",
            "Микроволновая печь",
            "Кухонная техника",
            "Торшер",
        ]

        for item in specifications_title:
            specifications, created = Specifications.objects.get_or_create(
                name="Тип устройства", value=item
            )

            self.stdout.write(
                "Created specifications: {name} | {value}\n".format(
                    name=specifications.name, value=specifications.value
                )
            )

        self.stdout.write(f"=== End of specifications creation ===")
