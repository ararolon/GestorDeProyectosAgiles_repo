# Generated by Django 4.1 on 2022-10-17 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Proyectos', '0001_initial'),
        ('UserStories', '0001_initial'),
        ('Usuarios', '0001_initial'),
        ('Sprint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprintmiembros',
            name='miembro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.usuario'),
        ),
        migrations.AddField(
            model_name='sprintmiembros',
            name='proyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Proyectos.proyecto'),
        ),
        migrations.AddField(
            model_name='sprintmiembros',
            name='sprint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Sprint.sprint'),
        ),
        migrations.AddField(
            model_name='sprintmiembros',
            name='us_asignado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UserStories.userstories'),
        ),
        migrations.AddField(
            model_name='sprint',
            name='historias',
            field=models.ManyToManyField(blank=True, to='UserStories.userstories'),
        ),
    ]
