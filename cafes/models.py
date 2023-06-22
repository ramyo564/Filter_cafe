from django.db import models
from common.models import CommonModel
from django.conf import settings


class Cafe(CommonModel):
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
        related_name="filler_reviews",
    )
