from django.db import models

# Create your models here.


class Filter(models.Model):
    class OptionChoices(models.TextChoices):
        PRODUCTIVITY = ("productivity", "Productivity")
        COMMUNITY = ("community", "Community")
        SERVICE = ("service", "Service")
        # ...

    option = models.CharField(choices=OptionChoices, max_length=20)

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FilterScore(models.Model):
    score = models.PositiveIntegerField()


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
    )
