import random

from django.core.management import BaseCommand

from order.models import Order, Payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Генерация платежей

        :param args:
        :param options:
        :return:
        """

        self.stdout.write("=== Start creating a payments ===")

        orders = Order.objects.all()
        orders_payments = random.sample(tuple(orders), k=random.randint(5, len(orders)))

        for order in orders_payments:
            card_number = random.randint(1000000000000000, 9999999999999999)

            payment, created = Payment.objects.get_or_create(
                order=order,
                number=card_number,
                name=order.fullName,
                month=str(random.randint(1, 12)),
                year=str(random.randint(2024, 2030)),
                code=str(random.randint(100, 999)),
            )

            order.status = "payment"
            order.save()

            self.stdout.write(
                " ".join(
                    [
                        "Created payment | order: #{order} | number: {number} | name: {name} |".format(
                            order=payment.order.pk,
                            number=payment.number,
                            name=payment.name,
                        ),
                        "month: {month} | year: {year} | code: {code}\n".format(
                            month=payment.month, year=payment.year, code=payment.code
                        ),
                    ]
                )
            )

        self.stdout.write("=== End of payments creation ===")
