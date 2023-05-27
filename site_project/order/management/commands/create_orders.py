import random

from django.core.management import BaseCommand

from authapp.models import User
from catalog.models import Product
from order.models import Order, OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Генерация заказов

        :param args:
        :param options:
        :return:
        """

        self.stdout.write("=== Start creating a orders ===")

        delivery_type = ("ordinary", "express")
        payment_type = ("online", "someone")

        citys = [
            "Друстэд",
            "Аочуаледо",
            "Урагларес",
            "Груигас",
            "Емуидвайн",
            "Уипруарон",
            "Афлеадган",
            "Кревер",
            "Фрезроувер",
            "Вридертон",
            "Цилас",
            "Уобефис",
            "Срафаст",
            "Жогларес",
            "Злорк",
            "Евлоамтон",
            "Ишоса",
            "Еутиеудейл",
            "Крул",
            "Шеуврелес",
        ]

        street_name_prefix = ("ул.", "пр.", "пл.")

        streets_names = [
            "победы",
            "красная",
            "зеленая",
            "синия",
            "желтая",
            "осения",
            "весеня",
            "летняя",
            "зимняя",
            "ленина",
            "чайковского",
            "достоевского",
            "бунина",
            "чайная",
            "сахарная",
            "мармиладная",
            "вафельеная",
            "разгровная",
            "стрелецкая",
            "пушкина",
        ]

        street_name_suffix = ["д.", "к.", "ст."]

        users = User.objects.all()
        products = Product.objects.all()

        for user in users:
            for _ in range(random.randint(1, 3)):
                address = " ".join(
                    [
                        "".join(
                            [
                                random.choice(street_name_prefix),
                                random.choice(streets_names).capitalize(),
                            ]
                        ),
                        "".join(
                            [
                                random.choice(street_name_suffix),
                                str(random.randint(1, 100)),
                            ]
                        ),
                    ]
                )

                order, created = Order.objects.get_or_create(
                    user=user,
                    fullName=user.fullName,
                    email=user.email,
                    phone=user.phone,
                    deliveryType=delivery_type[random.randint(0, 1)],
                    paymentType=payment_type[random.randint(0, 1)],
                    status="confirmed",
                    city=random.choice(citys),
                    address=address,
                )

                self.stdout.write(
                    " ".join(
                        [
                            "Created order | owner: [{owner}] | delivery: {delivery} | payment: {payment} |".format(
                                owner=" - ".join(
                                    [user.fullName, user.email, user.phone]
                                ),
                                delivery=order.deliveryType,
                                payment=order.paymentType,
                            ),
                            "status: {status} | city: {city} | address: {address}\n".format(
                                status=order.status,
                                city=order.city,
                                address=order.address,
                            ),
                        ]
                    )
                )

                self.stdout.write("Order products: ")

                for __ in range(random.randint(1, 5)):
                    product = random.choice(products)
                    quantity = random.randint(1, product.count)

                    order_item, created = OrderItem.objects.get_or_create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=quantity,
                    )

                    self.stdout.write(
                        "Created order product | product: {product} | price: {price} | quantity: {quantity} |".format(
                            product=order_item.product,
                            price=order_item.price,
                            quantity=order_item.quantity,
                        ),
                    )

                self.stdout.write("")

        self.stdout.write("=== End of orders creation ===")
