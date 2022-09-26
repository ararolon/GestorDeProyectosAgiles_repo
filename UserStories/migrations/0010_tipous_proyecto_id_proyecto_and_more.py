# Generated by Django 4.1 on 2022-09-25 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0009_userstories_id_proyecto'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipous_proyecto',
            name='id_proyecto',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='tipouserstory',
            name='descripcion',
            field=models.TextField(blank=True, max_length=80, null=True),
        ),
    ]