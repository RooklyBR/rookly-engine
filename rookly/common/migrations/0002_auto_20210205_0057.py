# Generated by Django 2.2.17 on 2021-02-05 00:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="business",
            unique_together={("user",)},
        ),
    ]
