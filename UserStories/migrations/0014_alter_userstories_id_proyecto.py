# Generated by Django 4.1 on 2022-09-25 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0013_alter_userstories_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstories',
            name='id_proyecto',
            field=models.IntegerField(),
        ),
    ]