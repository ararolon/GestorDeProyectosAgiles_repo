# Generated by Django 4.1 on 2022-10-15 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0013_sprintmiembros_proyecto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sprint',
            name='miembros_sprint',
        ),
    ]
