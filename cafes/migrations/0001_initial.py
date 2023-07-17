# Generated by Django 4.2.2 on 2023-07-17 12:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BusinessDays",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("day", models.CharField(max_length=10)),
            ],
            options={
                "verbose_name": "businessdays",
                "verbose_name_plural": "businessdays",
            },
        ),
        migrations.CreateModel(
            name="Cafe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("slug", models.SlugField(allow_unicode=True, max_length=255)),
                ("address", models.CharField(max_length=100)),
                ("img", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="CafeBusinessHours",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("business_hours", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="CafeOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.PositiveIntegerField(
                        default=10,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                ("sum_user", models.PositiveIntegerField(default=1)),
                ("sum_rating", models.PositiveBigIntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name="CafeReviews",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cafe_reviews", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cafe_reviews_cafe",
                        to="cafes.cafe",
                    ),
                ),
            ],
        ),
    ]
