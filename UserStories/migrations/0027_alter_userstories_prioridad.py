# Generated by Django 4.1 on 2022-10-13 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0026_userstories_en_sprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstories',
            name='Prioridad',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5),
        ),
    ]
