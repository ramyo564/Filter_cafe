from django.core.validators import MaxValueValidator
from django.db import models


class Cafe(models.Model):
    name = models.CharField(max_length=20)
    city = models.ForeignKey("filters.City", on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    business_hours = models.OneToOneField(
        "BusinessHours",
        on_delete=models.CASCADE,
    )
    img = models.URLField(max_length=200)  # 사진은 한장인가?
    # map = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Review(models.Model):
    cafe = models.ForeignKey(
        "cafes.Cafe",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(2)],
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class BusinessHours(models.Model):
    mon = models.CharField(max_length=50)
    tue = models.CharField(max_length=50)
    wed = models.CharField(max_length=50)
    thu = models.CharField(max_length=50)
    fri = models.CharField(max_length=50)
    sat = models.CharField(max_length=50)
    sun = models.CharField(max_length=50)

    def __str__(self):
        return (
            f"Monday: {self.mon}\n"
            f"Tuesday: {self.tue}\n"
            f"Wednesday: {self.wed}\n"
            f"Thursday: {self.thu}\n"
            f"Friday: {self.fri}\n"
            f"Saturday: {self.sat}\n"
            f"Sunday: {self.sun}"
        )
