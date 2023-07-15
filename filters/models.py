from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, allow_unicode=True)
    map = models.URLField(max_length=200)

    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class Filter(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, allow_unicode=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, allow_unicode=True)
    filter = models.ForeignKey("Filter", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
