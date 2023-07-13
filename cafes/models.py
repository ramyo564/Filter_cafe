from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from filters.models import City


class BusinessDays(models.Model):
    day = models.CharField(max_length=10)

    class Meta:
        verbose_name = "businessdays"
        verbose_name_plural = "businessdays"

    def __str__(self):
        return self.day


class Cafe(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    business_hours = models.ManyToManyField(
        BusinessDays,
        through="CafeBusinessHours",
        related_name="cafe_business_hours"
        )
    img = models.URLField(max_length=200)
    options = models.ManyToManyField(
        "filters.Option",
        through="CafeOption",
        related_name="cafe_options"
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    reviews = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reviews


class CafeOption(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name="cafe_option_cafe"
    )
    option = models.ForeignKey(
        "filters.Option",
        on_delete=models.CASCADE,
        related_name="cafe_option_option"
    )
    point = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        default=2
    )

    def __str__(self):
        return f"{self.cafe} - {self.option} - {self.point}"


class CafeBusinessHours(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name="cafe_business_hours_cafe"
    )
    business_days = models.ForeignKey(
        BusinessDays,
        on_delete=models.CASCADE,
        related_name="cafe_business_hours_bh"
    )
    business_hours = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cafe} - {self.business_days} - {self.business_hours}"
