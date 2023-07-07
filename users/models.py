from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    name = models.CharField(max_length=20, null=False, default="이름")
    age = models.IntegerField(null=True, blank=True, validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])
    gender = models.CharField(blank=True, max_length=10)

    def __str__(self):
        return self.name
