# Generated by Django 4.2.2 on 2023-07-04 02:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("filters", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="filter",
            name="img",
        ),
        migrations.RemoveField(
            model_name="filter",
            name="option",
        ),
    ]
