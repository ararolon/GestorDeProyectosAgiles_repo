# Generated by Django 4.1 on 2022-09-25 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Proyectos', '0020_proyecto_tipo_us'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='tipo_us',
        ),
    ]
