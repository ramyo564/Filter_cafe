from django.db import models


class Cafe(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    business_hours = models.CharField(max_length=100)
    img = models.URLField(max_length=200)
    map = models.URLField(max_length=200)
    options = models.ManyToManyField("filters.Option", related_name='cafes_options')
    reviews = models.ManyToManyField("users.User", through="Review")
    city = models.ForeignKey("filters.City", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Review(models.Model):
    cafe = models.ForeignKey("cafes.Cafe", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    rating = models.IntegerField()
    reviews = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reviews
