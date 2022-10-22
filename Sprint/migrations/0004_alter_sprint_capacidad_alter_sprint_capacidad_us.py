# Generated by Django 4.1 on 2022-10-20 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0003_alter_sprintmiembros_capacidad_miembro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='capacidad',
            field=models.IntegerField(blank=True, default=0, verbose_name='Capacidad en horas'),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='capacidad_us',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]