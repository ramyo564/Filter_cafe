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

    def __str__(self):
        return self.name


class Review(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    cafe_option = models.ForeignKey("CafeOption", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)]
    )
    reviews = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reviews

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cafe_option.sum_rating += self.rating
        self.cafe_option.sum_user += 1  # sum_user에 1 추가
        self.cafe_option.total_rating()  # 업데이트된 값을 기반으로 total_rating 호출
        self.cafe_option.save()  # CafeOption 모델 저장


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
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        default=2
    )
    sum_user = models.PositiveIntegerField(
        default=1
    )
    sum_rating = models.PositiveBigIntegerField(
        default=2
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
