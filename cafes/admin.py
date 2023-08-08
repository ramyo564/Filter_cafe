from django.contrib import admin

from .models import Cafe, BusinessDays, CafeBusinessHours, CafeOption, CafeReviews

# Register your models here.


class CafeOptionInline(admin.TabularInline):
    model = CafeOption


class CafeBusinessHoursInline(admin.TabularInline):
    model = CafeBusinessHours


class CafeReviewsInline(admin.TabularInline):
    model = CafeReviews


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    inlines = [CafeOptionInline, CafeBusinessHoursInline, CafeReviewsInline]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(BusinessDays)
