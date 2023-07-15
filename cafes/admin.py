from django.contrib import admin

from .models import Cafe, Review, BusinessDays, CafeBusinessHours, CafeOption

# Register your models here.


class CafeOptionInline(admin.TabularInline):
    model = CafeOption


class CafeBusinessHoursInline(admin.TabularInline):
    model = CafeBusinessHours


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    inlines = [CafeOptionInline, CafeBusinessHoursInline]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Review)
admin.site.register(BusinessDays)
