# Generated by Django 4.1 on 2022-09-29 02:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0004_sprint_capacidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de creación'),
        ),
    ]
