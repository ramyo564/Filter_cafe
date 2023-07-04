from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.


class Filter(models.Model):
    """
    어떻게 해야 할지 몰라서 주석 처리.
    OptionChoices = [
        ("productivity", "Productivity"),
        ("community", "Community"),
        ("service", "Service"),
    ]
    option = models.CharField(choices=OptionChoices, max_length=20)
    img = models.URLField(max_length=200)
    """

    name = models.CharField(
        max_length=50,
        unique=True,
    )

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
