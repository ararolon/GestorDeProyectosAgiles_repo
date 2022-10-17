# Generated by Django 4.1 on 2022-10-17 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Sprint', '0002_initial'),
        ('UserStories', '0002_initial'),
        ('Proyectos', '0002_initial'),
        ('permisos', '0001_initial'),
        ('Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolusuario',
            name='roles',
            field=models.ManyToManyField(to='permisos.rolesdesistema'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='miembros',
            field=models.ManyToManyField(related_name='set_miembros', to='Usuarios.usuario'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='roles',
            field=models.ManyToManyField(to='permisos.rolesdesistema'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='scrumMaster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.usuario'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='sprint',
            field=models.ManyToManyField(to='Sprint.sprint'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='tipo_us',
            field=models.ManyToManyField(to='UserStories.tipouserstory'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='usuario_roles',
            field=models.ManyToManyField(to='Proyectos.rolusuario'),
        ),
    ]
