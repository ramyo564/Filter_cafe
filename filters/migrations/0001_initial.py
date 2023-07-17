# Generated by Django 4.2.2 on 2023-07-17 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(allow_unicode=True, max_length=255)),
                ("map", models.URLField()),
            ],
            options={
                "verbose_name": "city",
                "verbose_name_plural": "cities",
            },
        ),
        migrations.CreateModel(
            name="Filter",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(allow_unicode=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Option",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(allow_unicode=True, max_length=255)),
                (
                    "filter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="filters.filter"
                    ),
                ),
            ],
        ),
    ]
