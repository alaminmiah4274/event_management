# Generated by Django 5.1.5 on 2025-02-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0006_remove_event_user_profile_delete_participant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="event",
            field=models.ManyToManyField(related_name="participant", to="tasks.event"),
        ),
    ]
