from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    name = models.CharField(max_length=20, null=False, default="이름")
    age = models.IntegerField(null=True, blank=True, validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])
    gender = models.CharField(blank=True, max_length=10)

    def __str__(self):
        return self.name


class UserRating(models.Model):
    cafe = models.ForeignKey("cafes.Cafe", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    cafe_option = models.ForeignKey("cafes.CafeOption", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.cafe_option} - {self.rating}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cafe_option.sum_rating += int(self.rating)
        self.cafe_option.sum_user += 1  # sum_user에 1 추가
        self.cafe_option.total_rating()  # 업데이트된 값을 기반으로 total_rating 호출
        self.cafe_option.save()  # CafeOption 모델 저장
