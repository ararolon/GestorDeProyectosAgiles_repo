# Generated by Django 4.1 on 2022-09-25 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0013_alter_userstories_tipo'),
        ('Proyectos', '0019_remove_proyecto_tipo_us_remove_proyecto_user_stories'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='tipo_us',
            field=models.ManyToManyField(to='UserStories.tipouserstory'),
        ),
    ]
