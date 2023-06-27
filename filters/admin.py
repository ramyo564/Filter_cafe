from django.contrib import admin

from .models import BallotBox, Filter, FilterScore

# Register your models here.


admin.site.register(Filter)
admin.site.register(FilterScore)
admin.site.register(BallotBox)
