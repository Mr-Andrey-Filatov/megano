import os
import random
from pathlib import Path
from django.core.files import File
from string import ascii_letters, digits, punctuation
from typing import Dict
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from authapp.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("users_count", type=int, choices=range(10, 101))

    def handle(self, *args, **options):
        self.stdout.write("=== Creating users ===")

        with open(
            "./authapp/management/commands/report.txt", "w", encoding="utf-8"
        ) as report:
            report.write("Generated user data:\n")

            admins = 0
            max_admins = random.randint(2, 5)

            for count in range(1, options["users_count"] + 1):
                user_data, avatar = (
                    self.superuser_data_generation()
                    if count == 1
                    else self.user_data_generation()
                )

                user = (
                    User.objects.create_superuser(**user_data)
                    if count == 1
                    else User.objects.create_user(**user_data)
                )

                if (count > 1) and (admins <= max_admins):
                    user.is_staff = True
                    admins += 1

                avatar_path = Path(avatar)

                with avatar_path.open(mode="rb") as f:
                    user.avatar = File(f, name=avatar_path.name)
                    user.save()

                report.write(
                    "{fullName} | {username} | {password} | admin: {is_staff} | superuser: {is_superuser}\n".format(
                        fullName=user.fullName,
                        username=user.username,
                        password=user_data["password"],
                        is_staff=user.is_staff,
                        is_superuser=user.is_superuser,
                    )
                )

                self.stdout.write(
                    "".join(
                        [
                            "User created: {fullName} | is_staff: {is_staff} | ".format(
                                fullName=user.fullName,
                                is_staff=user.is_staff,
                            ),
                            "superuser: {is_superuser} | avatar: {avatar}\n".format(
                                is_superuser=user.is_superuser,
                                avatar=user.avatar.name,
                            ),
                        ]
                    )
                )

        self.stdout.write("=== End of users creation ===")

    def superuser_data_generation(self) -> tuple:
        """
        Генерация данных супер пользователя

        :return:
        """

        avatars_admin_samples_path = os.path.join(
            os.getcwd(),
            "frontend/static/frontend/assets/img/media_user/profile_sample/superuser/",
        )

        photos_samples_names = list(
            map(
                lambda photo_name: os.path.join(avatars_admin_samples_path, photo_name),
                os.listdir(avatars_admin_samples_path),
            )
        )

        random.shuffle(photos_samples_names)

        return self.check_user_data(
            dict(
                fullName=" ".join(
                    [
                        "Admin",
                        "Adminov",
                    ]
                ),
                first_name="Admin",
                last_name="Adminov",
                username="admin",
                email="admin@super.user",
                password="".join(
                    random.choices(digits + ascii_letters + punctuation, k=8)
                ),
                phone=str(random.randint(79000000000, 80000000000)),
            )
        ), random.choice(photos_samples_names)

    def user_data_generation(self) -> tuple:
        """
        Генерация данных пользователя

        :return:
        """

        names = [
            (
                ("anastasia", "Анастасия"),
                ("daria", "Дарья"),
                ("maria", "Мария"),
                ("anna", "Анна"),
                ("victoria", "Виктория"),
                ("pauline", "Полина"),
                ("elizabeth", "Елизавета"),
                ("catherine", "Екатерина"),
                ("ksenia", "Ксения"),
                ("valeria", "Валерия"),
            ),
            (
                ("alexander", "Александр"),
                ("boris", "Борис"),
                ("vadim", "Вадим"),
                ("denis", "Денис"),
                ("ivan", "Иван"),
                ("oleg", "Олег"),
                ("paul", "Павел"),
                ("novel", "Роман"),
                ("stanislav", "Станислав"),
                ("yuri", "Юрий"),
            ),
        ]

        surnames = [
            (
                ("orlova", "Орлова"),
                ("lebedev", "Лебедева"),
                ("simonova", "Симонова"),
                ("alexandrova", "Александрова"),
                ("tretyakova", "Третьякова"),
                ("lenskaya", "Ленская"),
                ("kamensky", "Каменских"),
                ("kozhevnikova", "Кожевникова"),
                ("denisova", "Денисова"),
                ("andreeva", "Андреева"),
            ),
            (
                ("ivanov", "Иванов"),
                ("smirnov", "Смирнов"),
                ("kuznetsov", "Кузнецов"),
                ("popov", "Попов"),
                ("vasiliev", "Васильев"),
                ("petrov", "Петров"),
                ("sokolov", "Соколов"),
                ("mikhailov", "Михайлов"),
                ("novikov", "Новиков"),
                ("fedorov", "Фёдоров"),
            ),
        ]

        domain_names = [
            "naquk",
            "lofyvax",
            "vukof",
            "rylip",
            "vofug",
            "moqor",
            "ydo",
            "muwob",
            "evexu",
            "gexit",
        ]

        consonants = (
            "b",
            "c",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "l",
            "m",
            "n",
            "p",
            "q",
            "r",
            "s",
            "t",
            "v",
            "w",
            "x",
            "y",
            "z",
        )

        vowels = ("a", "e", "i", "o", "u", "y")

        avatars_female_samples_path = os.path.join(
            os.getcwd(),
            "frontend/static/frontend/assets/img/media_user/profile_sample/female/",
        )

        avatars_male_samples_path = os.path.join(
            os.getcwd(),
            "frontend/static/frontend/assets/img/media_user/profile_sample/male/",
        )

        photos_samples_names = [
            list(
                map(
                    lambda photo_name: os.path.join(
                        avatars_female_samples_path, photo_name
                    ),
                    os.listdir(avatars_female_samples_path),
                )
            ),
            list(
                map(
                    lambda photo_name: os.path.join(
                        avatars_male_samples_path, photo_name
                    ),
                    os.listdir(avatars_male_samples_path),
                )
            ),
        ]

        random.shuffle(photos_samples_names[0])
        random.shuffle(photos_samples_names[1])

        sex = random.randint(0, 1)

        user_names = random.choice(names[sex])
        user_surnames = random.choice(surnames[sex])

        username = random.choice(("", "_")).join(
            [
                (
                    user_names[0].capitalize()
                    if random.getrandbits(1)
                    else user_names[0]
                )[: random.randint(1, len(user_names[0]))],
                (
                    user_surnames[0].capitalize()
                    if random.getrandbits(1)
                    else user_surnames[0]
                )[: random.randint(2, len(user_surnames[0]))],
            ][random.randint(0, 1) :: random.randint(1, 2)]
        )

        email = "".join(
            [
                random.choice(("", "_")).join([user_names[0], user_surnames[0]]),
                "@",
                random.choice(domain_names),
                ".",
                "".join(
                    [
                        "".join([random.choice(consonants), random.choice(vowels)])
                        for _ in range(1, 3)
                    ]
                )[: random.randint(2, 3)],
            ]
        )

        random.shuffle(photos_samples_names[sex])

        return self.check_user_data(
            dict(
                fullName=" ".join(
                    [
                        user_names[1],
                        user_surnames[1],
                    ]
                ),
                first_name=user_names[1],
                last_name=user_surnames[1],
                username=username,
                email=email,
                password="".join(
                    random.choices(digits + ascii_letters + punctuation, k=8)
                ),
                phone=str(random.randint(79000000000, 80000000000)),
            )
        ), random.choice(photos_samples_names[sex])

    @staticmethod
    def check_user_data(user_data: Dict) -> Dict:
        """
        Проверка на наличие пользователя с передаными данными

        :param user_data:
        :return:
        """

        buffer = user_data.copy()

        while True:
            if (
                (not User.objects.filter(username=buffer["username"]).exists())
                and (not User.objects.filter(email=buffer["email"]).exists())
                and (not User.objects.filter(phone=buffer["phone"]).exists())
            ):
                return buffer.copy()

            buffer["username"] = random.choice(("", "_")).join(
                [user_data["username"], str(random.randint(1, 10000))]
            )

            buffer["email"] = random.choice(("", "_")).join(
                [user_data["email"], str(random.randint(1, 10000))]
            )

            buffer["phone"] = str(random.randint(79000000000, 80000000000))
