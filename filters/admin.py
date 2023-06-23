from django.contrib import admin

from .models import City, Filter, Option

# Register your models here.


admin.site.register(City)
admin.site.register(Filter)
admin.site.register(Option)
