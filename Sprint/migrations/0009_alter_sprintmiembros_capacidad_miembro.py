# Generated by Django 4.1 on 2022-11-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0008_merge_20221102_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprintmiembros',
            name='capacidad_miembro',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
