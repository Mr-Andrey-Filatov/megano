from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


def profile_avatar_directory_path(instance: "User", filename: str) -> str:
    return "profiles/profile_{pk}/avatar/{filename}".format(
        pk=instance.pk, filename=filename
    )


class User(AbstractUser):
    def validate_image(fieldfile_obj):
        file_size = fieldfile_obj.size
        megabyte_limit = 150.0
        if file_size > megabyte_limit * 1024 * 1024:
            raise ValidationError(
                "Максимальный размер файла {}MB".format(str(megabyte_limit))
            )

    fullName = models.CharField(
        default="не указано", max_length=50, verbose_name="ФИО пользователя", blank=True
    )
    phone = models.CharField(
        default="Не указано",
        max_length=30,
        verbose_name="номер телефона",
        blank=True,
        null=True,
        unique=True,
    )
    email = models.EmailField(
        verbose_name="email пользователя", blank=True, unique=True
    )
    avatar = models.ImageField(
        upload_to=profile_avatar_directory_path,
        null=True,
        validators=[validate_image],
        default="",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.fullName
