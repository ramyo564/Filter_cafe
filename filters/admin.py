from django.contrib import admin

from .models import City, Filter, Option

# Register your models here.


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


class FilterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "city", "slug")
    ordering = ("city",)


class OptionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "filter", "slug")
    ordering = ("filter__city",)


admin.site.register(City, CityAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Option, OptionAdmin)
