import decimal
import random

from django.core.management import BaseCommand

from catalog.models import SaleItem, Product
from datetime import datetime, timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Генерация распродаж

        :param args:
        :param options:
        :return:
        """

        self.stdout.write(f"=== Start creating a sales ===")

        products = Product.objects.all()
        products_sales = random.sample(
            tuple(products), k=random.randint(5, len(products))
        )

        for product in products_sales:
            discount = random.randint(10, 50)
            sale_price = round(
                product.price - (product.price * decimal.Decimal(discount / 100)), 2
            )

            cur_date = datetime.now()
            date_from = cur_date + timedelta(days=random.randint(0, 10))
            date_to = date_from + timedelta(days=random.randint(3, 365))

            sale, created = SaleItem.objects.get_or_create(
                salePrice=sale_price,
                dateFrom=date_from.date(),
                dateTo=date_to.date(),
                product=product,
            )

            self.stdout.write(
                " ".join(
                    [
                        "Created sale: title: {title} | price: {price} | salePrice: {salePrice} |".format(
                            title=sale,
                            price=sale.product.price,
                            salePrice=sale.salePrice,
                        ),
                        "dateFrom: {dateFrom} | dateTo: {dateTo} | href: {href}\n".format(
                            dateFrom=sale.dateFrom,
                            dateTo=sale.dateTo,
                            href=sale.href(),
                        ),
                    ]
                )
            )

        self.stdout.write(f"=== End of sales creation ===")
