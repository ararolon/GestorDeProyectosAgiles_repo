# Generated by Django 4.1 on 2022-09-24 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyectos', '0005_rename_miembros_rolusuario_miembro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(choices=[('En Planificacion', 'En Planificacion'), ('En curso', 'En Curso'), ('Finalizado', 'Finalizado'), ('Cancelado', 'Cancelado')], default='En Planificacion', max_length=20),
        ),
    ]