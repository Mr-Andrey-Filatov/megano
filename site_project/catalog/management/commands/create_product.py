import decimal
import os
import random
from pathlib import Path
from django.core.files import File
from django.core.management import BaseCommand
from catalog.models import (
    CategoryProduct,
    Specifications,
    Tags,
    Product,
    ProductImage,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("products_count", type=int, choices=range(10, 201))

    def handle(self, *args, **options):
        """
        Генерация продуктов

        :param args:
        :param options:
        :return:
        """

        self.stdout.write(f"=== Start creating a products ===")

        products_titles = [
            "Arctic",
            "Barand",
            "Business",
            "Carbide",
            "Corsair",
            "Drones",
            "Hobby",
            "Mavic",
            "Mini",
            "New",
            "PRO",
            "Phone",
            "Quadcopter",
            "RC",
            "Series",
            "Smart",
            "Steel",
            "White",
        ]

        product_description = """Megano Store Hystory Lorem ipsum dolor sit amet, consectetuer adipiscing elit doli. 
        Aenean commodo ligula eget dolor. Aenean massa. Cumtipsu sociis natoque penatibus et magnis dis parturient 
        montesti, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eutu, pretiumem. Lorem ipsum 
        dolor sit amet, consectetuer adipiscing elit doli. Aenean commodo ligula eget dolor. Aenean massa. Cumtipsu 
        sociis natoque penatibus et magnis dis parturient montesti, nascetur ridiculus mus. Donec quam felis, ultricies 
        nec, pellentesque eutu""".split()

        photos_samples_path = os.path.join(
            os.getcwd(),
            "frontend/static/frontend/assets/img/media_user/product_sample/",
        )

        photos_samples_names = list(
            map(
                lambda photo_name: os.path.join(photos_samples_path, photo_name),
                os.listdir(photos_samples_path),
            )
        )

        specifications = Specifications.objects.all()
        categories = CategoryProduct.objects.all()
        tags = Tags.objects.all()

        for _ in range(1, options["products_count"] + 1):
            title = " ".join(random.choices(products_titles, k=random.randint(2, 5)))

            if random.getrandbits(1):
                title = " ".join([title, str(random.randint(1, 10000))])

            product, created = Product.objects.get_or_create(
                title=title,
                description=" ".join(
                    random.choices(
                        product_description,
                        k=random.randint(10, len(product_description)),
                    )
                ),
                count=random.randint(1, 10),
                price=decimal.Decimal(random.randrange(10000, 50000)) / 100,
                free_delivery=random.getrandbits(1),
                rating=random.randint(1, 10),
                specifications=random.choice(specifications),
                category=random.choice(categories),
                available=random.getrandbits(1),
                limited=random.getrandbits(1),
            )

            product.tags.add(*random.choices(tags, k=random.randint(1, len(tags))))
            product.save()

            self.stdout.write(
                "".join(
                    [
                        "Created product: {title} | count: {count} | price: {price} | ".format(
                            title=product.title,
                            count=product.count,
                            price=product.price,
                        ),
                        "free_delivery: {free_delivery} | rating: {rating} | ".format(
                            free_delivery=product.free_delivery,
                            rating=product.rating,
                        ),
                        "category: {category} | available: {available} | limited: {limited}\n".format(
                            category=product.category,
                            available=product.available,
                            limited=product.limited,
                        ),
                    ]
                )
            )

            random.shuffle(photos_samples_names)

            product_images = photos_samples_names[: random.randint(2, 5)]

            random.shuffle(product_images)

            for image_path in product_images:
                path = Path(image_path)

                with path.open(mode="rb") as f:
                    product_image, created = ProductImage.objects.get_or_create(
                        product=product, image=File(f, name=path.name)
                    )

                self.stdout.write(f"Created product image {product_image.image.name}")

            self.stdout.write()

        self.stdout.write(f"=== End of products creation ===")
