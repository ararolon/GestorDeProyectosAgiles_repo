# Generated by Django 4.1 on 2022-10-12 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0023_userstories_prioridad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstories',
            name='Prioridad',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
