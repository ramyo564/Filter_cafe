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
    slug = models.SlugField(max_length=255, allow_unicode=True)
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
    cafe_reviews = models.ManyToManyField(
        "users.User",
        through="CafeReviews",
        related_name="cafe_user_reviews"
    )

    def __str__(self):
        return self.name


class CafeOption(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name="cafe_option_cafe"
    )
    cafe_option = models.ForeignKey(
        "filters.Option",
        on_delete=models.CASCADE,
        related_name="cafe_option_option"
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=10
    )
    sum_user = models.PositiveIntegerField(
        default=1
    )
    sum_rating = models.PositiveBigIntegerField(
        default=10
    )

    def __str__(self):
        return f"{self.cafe} - {self.cafe_option} - total user: {self.sum_user}\n" \
            f"- total rating: {self.sum_rating}"

    def total_rating(self):
        if self.sum_user != 0:
            self.rating = self.sum_rating // self.sum_user
        else:
            self.rating = 0
        self.save()


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


class CafeReviews(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name="cafe_reviews_cafe"
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="cafe_reviews_user"
    )
    cafe_reviews = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cafe.name} - {self.user.name} - {self.cafe_reviews}"
