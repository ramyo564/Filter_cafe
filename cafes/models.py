from django.db import models


class Cafe(models.Model):
    name = models.CharField(max_length=20)
    CityChoices = [
        ("서울", "서울"),
        ("인천", "인천"),
        ("부산", "부산"),
    ]

    city = models.CharField(
        max_length=20,
        choices=CityChoices,
    )
    address = models.CharField(max_length=100)
    business_hours = models.CharField(max_length=100)
    img = models.URLField(max_length=200)  # 사진은 한장인가?

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
    rating = models.PositiveIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
