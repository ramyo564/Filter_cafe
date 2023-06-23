from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Filler(models.Model):
    name = models.CharField(max_length=50, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=50)
    filter = models.ForeignKey(Filler, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
