# Generated by Django 4.1 on 2022-09-20 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0002_userstories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipouserstory',
            name='prefijo',
        ),
    ]
