# Generated by Django 4.1 on 2022-11-19 17:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HoraPorDia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horas', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ('dia', models.IntegerField()),
                ('user_story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horas_por_dia', to='UserStories.userstories')),
            ],
            options={
                'verbose_name': 'HoraPorDia',
                'verbose_name_plural': 'HorasPorDia',
            },
        ),
    ]