from django.db import models
from common.models import CommonModel


class Review(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    content = models.TextField()
