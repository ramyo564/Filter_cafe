from django.contrib import admin

from .models import BallotBox, Filter, FilterScore

# Register your models here.


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


class FilterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


class OptionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "filter", "slug")
    ordering = ("filter",)


admin.site.register(City, CityAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Option, OptionAdmin)
