# Generated by Django 4.1 on 2022-11-02 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyectos', '0004_historia_proyecto_historial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historia',
            name='evento',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]