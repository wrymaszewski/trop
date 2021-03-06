# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-10 22:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('location', location_field.models.plain.PlainLocationField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Top',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_type', models.CharField(choices=[('SP', 'Single-Pitch'), ('MP', 'Multi-Pitch'), ('BLD', 'Boulder')], max_length=100)),
                ('scale', models.CharField(choices=[('YDS', 'YDS'), ('FR', 'French'), ('UIAA', 'UIAA'), ('POL', 'Polish'), ('V', 'Verm')], default='FR', max_length=100)),
                ('grade', models.CharField(max_length=10)),
                ('ascent_style', models.CharField(choices=[('OS', 'OS'), ('FL', 'Flash'), ('RP', 'RP'), ('PP', 'PP'), ('AF', 'AF'), ('TR', 'TR')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to='indoor.Gym')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='top',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tops', to='indoor.Training'),
        ),
    ]
