# Generated by Django 4.1 on 2022-09-29 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0006_alter_sprint_fecha_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='id_proyecto',
            field=models.IntegerField(null=True),
        ),
    ]