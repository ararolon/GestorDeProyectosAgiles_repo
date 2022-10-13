# Generated by Django 4.1 on 2022-10-12 00:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0021_alter_userstories_horas_estimadas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstories',
            name='horas_estimadas',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
