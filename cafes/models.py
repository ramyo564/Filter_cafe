from django.db import models


class Cafe(models.Model):
    class CityChoices(models.TextChoices):
        SEOUL = ("서울", "서울")
        INCHEON = ("인천", "인천")
        BUSAN = ("부산", "부산")

    city = models.CharField(choices=CityChoices, max_length=20)

    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    business_hours = models.CharField(max_length=100)
    img = models.URLField(max_length=200)
    map = models.URLField(max_length=200)

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
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
