from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=20, null=False, default="이름")

    def __str__(self):
        return self.name
