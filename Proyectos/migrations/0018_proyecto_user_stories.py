# Generated by Django 4.1 on 2022-09-25 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0009_userstories_id_proyecto'),
        ('Proyectos', '0017_proyecto_tipo_us'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='user_stories',
            field=models.ManyToManyField(to='UserStories.userstories'),
        ),
    ]
