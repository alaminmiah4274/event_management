# Generated by Django 5.1.5 on 2025-02-02 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.DateTimeField()),
                ('location', models.CharField(max_length=250)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='tasks.category')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('event', models.ManyToManyField(related_name='participant', to='tasks.event')),
            ],
        ),
    ]
