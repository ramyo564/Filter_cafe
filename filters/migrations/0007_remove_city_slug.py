# Generated by Django 4.2.2 on 2023-07-09 12:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("filters", "0006_city_option_filter_option"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="city",
            name="slug",
        ),
    ]
