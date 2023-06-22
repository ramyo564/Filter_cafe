from django.db import models
from common.models import CommonModel
from django.conf import settings


class Cafe(CommonModel):
    class CityChoices(models.TextChoices):
        SEOUL = ("서울", "서울")
        BUSAN = ("부산", "부산")
        INCHEON = ("인천", "인천")

    kind = models.CharField(
        max_length=20,
        choices=CityChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=50,
    )
    address = models.TextField()
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="like_cafes",
    )
    filler = models.ManyToManyField(
        "fillers.Filler",
        related_name="filler_cafes",
    )
