# Generated by Django 4.1 on 2022-10-20 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0004_alter_sprint_capacidad_alter_sprint_capacidad_us'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprintmiembros',
            name='capacidad_miembro',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]