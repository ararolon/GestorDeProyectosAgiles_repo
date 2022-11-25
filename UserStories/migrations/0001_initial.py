# Generated by Django 4.1 on 2022-11-25 00:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estados_Kanban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('defecto', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Estado_Kanban',
                'verbose_name_plural': 'Estados_Kanban',
            },
        ),
        migrations.CreateModel(
            name='HistoricalUserStories',
            fields=[
                ('id_us', models.IntegerField(blank=True, db_index=True)),
                ('id_proyecto', models.IntegerField(null=True)),
                ('nombre', models.CharField(db_index=True, max_length=20)),
                ('descripcion', models.TextField(blank=True, max_length=60)),
                ('comentarios', models.TextField(blank=True, default='')),
                ('horas_estimadas', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('PN', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('PT', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('PS', models.IntegerField(blank=True, default=0)),
                ('Prioridad', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5)),
                ('motivo_cancelacion', models.TextField(blank=True, max_length=60)),
                ('en_sprint', models.BooleanField(default=False)),
                ('horas_trabajadas', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('actividad', models.CharField(blank=True, max_length=50, null=True)),
                ('horas', models.IntegerField(blank=True, default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical UserStory',
                'verbose_name_plural': 'historical UserStories',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HoraPorDia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horas', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ('dia', models.IntegerField()),
            ],
            options={
                'verbose_name': 'HoraPorDia',
                'verbose_name_plural': 'HorasPorDia',
            },
        ),
        migrations.CreateModel(
            name='TipoUSerStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('descripcion', models.TextField(blank=True, max_length=80, null=True)),
            ],
            options={
                'verbose_name': 'TipoUS',
                'verbose_name_plural': 'TiposUS',
            },
        ),
        migrations.CreateModel(
            name='UserStories',
            fields=[
                ('id_us', models.AutoField(primary_key=True, serialize=False)),
                ('id_proyecto', models.IntegerField(null=True)),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('descripcion', models.TextField(blank=True, max_length=60)),
                ('comentarios', models.TextField(blank=True, default='')),
                ('horas_estimadas', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('PN', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('PT', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('PS', models.IntegerField(blank=True, default=0)),
                ('Prioridad', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5)),
                ('motivo_cancelacion', models.TextField(blank=True, max_length=60)),
                ('en_sprint', models.BooleanField(default=False)),
                ('horas_trabajadas', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('actividad', models.CharField(blank=True, max_length=50, null=True)),
                ('horas', models.IntegerField(blank=True, default=0)),
                ('estado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UserStories.estados_kanban')),
            ],
            options={
                'verbose_name': 'UserStory',
                'verbose_name_plural': 'UserStories',
            },
        ),
    ]
