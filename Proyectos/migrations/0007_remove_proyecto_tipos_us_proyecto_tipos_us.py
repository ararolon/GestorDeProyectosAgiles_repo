# Generated by Django 4.1 on 2022-09-22 18:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyectos', '0006_remove_proyecto_tipos_us_proyecto_tipos_us'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='tipos_us',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='tipos_us',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=None),
        ),
    ]
