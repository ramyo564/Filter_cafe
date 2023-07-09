from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=20, null=False, default="이름")
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(100)],
    )
    gender = models.CharField(
        null=True,
        blank=True,
        max_length=10,
    )

    def __str__(self):
        return self.name
