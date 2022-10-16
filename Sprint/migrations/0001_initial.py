# Generated by Django 4.1 on 2022-10-16 22:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_sprint', models.CharField(max_length=100)),
                ('nombre_sprint', models.CharField(max_length=100, unique=True)),
                ('duracion_sprint', models.IntegerField(blank=True, null=True, verbose_name='Duración del sprint')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de creación')),
                ('fecha_inicio', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de inicio')),
                ('fecha_fin', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de fin')),
                ('descripcion', models.TextField(blank=True, default='', max_length=200)),
                ('estado_sprint', models.CharField(choices=[('En Planificacion', 'En Planificacion'), ('En Curso', 'En Ejecucion'), ('Finalizado', 'Finalizado'), ('Cancelado', 'Cancelado')], default='En Planificacion', max_length=20)),
                ('id_proyecto', models.IntegerField(null=True)),
                ('capacidad', models.IntegerField(null=True, verbose_name='Capacidad en horas')),
                ('capacidad_us', models.IntegerField(default=0)),
            ],
        ),
    ]
