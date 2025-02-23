# Generated by Django 5.1.5 on 2025-02-22 17:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0004_alter_event_asset"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="user",
            field=models.ManyToManyField(
                related_name="event", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
