from django.core.validators import MaxValueValidator
from django.db import models


class Filter(models.Model):
    option = models.ForeignKey(
        "Option",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    # is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FilterScore(models.Model):
    score = models.PositiveIntegerField(
        unique=True,
        validators=[MaxValueValidator(100)],
    )


class BallotBox(models.Model):
    cafe = models.ForeignKey(
        "cafes.Cafe",
        on_delete=models.CASCADE,
        related_name="ballot_boxs",
    )
    filter = models.ForeignKey(
        "filters.Filter",
        on_delete=models.CASCADE,
        related_name="ballot_boxs",
    )
    score = models.ForeignKey(
        "filters.FilterScore",
        on_delete=models.CASCADE,
        related_name="ballot_boxs",
    )
    users = models.ManyToManyField(
        "users.User",
        related_name="ballot_boxs",
        blank=True,
        null=True,
    )


class City(models.Model):
    name = models.CharField(max_length=50)
    # slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name
