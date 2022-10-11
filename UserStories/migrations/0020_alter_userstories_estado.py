# Generated by Django 4.1 on 2022-10-07 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserStories', '0019_userstories_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstories',
            name='estado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UserStories.estados_kanban'),
        ),
    ]