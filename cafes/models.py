from django.db import models

from filters.models import City, Option
from users.models import User


class Cafe(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    business_hours = models.CharField(max_length=100)
    img = models.URLField(max_length=200)
    map = models.URLField(max_length=200)
    options = models.ManyToManyField(Option, related_name='cafes_options')
    reviews = models.ManyToManyField(User, through="Review")
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Review(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    reviews = models.TextField()

    def __str__(self):
        return self.name
