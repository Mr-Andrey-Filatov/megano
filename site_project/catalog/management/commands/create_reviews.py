import random

from django.core.management import BaseCommand

from authapp.models import User
from catalog.models import Review, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Генерация отзывы

        :param args:
        :param options:
        :return:
        """

        words = """a acquitted best bright buy color completed corresponds declared delight delivery description device 
        expectations expected experienced fast find gave gentle good great ideal impeccably it less lies like liked 
        little looks material money no order out perfect photo pleases price product properly purchase qualitative 
        qualitatively quality real regret regretted rich satisfied seemed shades silently size small some take thank 
        the turned use very wear wore works you""".split()

        users = User.objects.all()
        products = Product.objects.all()

        self.stdout.write(f"=== Start creating a reviews ===")

        for _ in range(1, random.randint(30, 50)):
            user_random = random.choice(users)
            review, created = Review.objects.get_or_create(
                author=user_random.fullName,
                email=user_random.email,
                text=" ".join(
                    random.choices(words, k=random.randint(5, 20))
                ).capitalize(),
                rate=random.randint(1, 5),
                product=random.choice(products),
            )

            self.stdout.write(
                " ".join(
                    [
                        "Created review | author: {author} | email: {email} | text: {text} |".format(
                            author=review.author,
                            email=review.email,
                            text=review.text[:15],
                        ),
                        "rate: {rate} | date: {date} | product: {product}\n".format(
                            rate=review.rate, date=review.date, product=review.product
                        ),
                    ]
                )
            )

        self.stdout.write(f"=== End of reviews creation ===")
