# Generated by Django 4.1 on 2022-09-22 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('UserStories', '0003_remove_tipouserstory_prefijo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_sprint', models.CharField(max_length=100)),
                ('nombre_sprint', models.CharField(max_length=100, unique=True)),
                ('duracion_sprint', models.IntegerField(blank=True, null=True, verbose_name='Duración del sprint')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de fin')),
                ('descripcion', models.TextField(blank=True, default='', max_length=200)),
                ('estado_sprint', models.CharField(choices=[('En Planificacion', 'En Planificacion'), ('En curso', 'En Ejecucion'), ('Finalizado', 'Finalizado'), ('Cancelado', 'Cancelado')], default='En Planificacion', max_length=20)),
                ('historias', models.ManyToManyField(blank=True, to='UserStories.userstories')),
            ],
        ),
    ]
