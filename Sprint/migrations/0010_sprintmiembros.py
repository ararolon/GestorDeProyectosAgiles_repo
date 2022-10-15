# Generated by Django 4.1 on 2022-10-14 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0027_alter_userstories_prioridad'),
        ('Usuarios', '0001_initial'),
        ('Sprint', '0009_remove_sprint_contador_sprint_activo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SprintMiembros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacidad_miembro', models.IntegerField(null=True)),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.usuario')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sprint.sprint')),
                ('us_asignado', models.ManyToManyField(to='UserStories.userstories')),
            ],
        ),
    ]