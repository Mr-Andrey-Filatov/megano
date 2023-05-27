from django.core.management import BaseCommand

from catalog.models import Tags


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Генерация тегов

        :param args:
        :param options:
        :return:
        """

        self.stdout.write(f"=== Start creating a tags ===")

        tags_names = [
            "Video",
            "Development",
            "Games",
            "Asus",
            "TV",
            "Headphones",
            "Washing machine",
            "Accessory",
            "Hood",
            "Electronics",
            "Camera",
            "Findings",
            "Mobile phone",
            "Bag",
            "Microwave",
            "Kitchen appliances",
            "Floor lamp",
        ]

        for tags_name in tags_names:
            tag, created = Tags.objects.get_or_create(name=tags_name)

            self.stdout.write(
                "Created tag: {name}\n".format(
                    name=tag.name,
                )
            )

        self.stdout.write(f"=== End of tags creation ===")
