from django.db import models
from common.models import CommonModel


class Filler(CommonModel):
    filler_name = models.CharField(max_length=50, unique=True)
