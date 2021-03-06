# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-05 08:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_auto_20180204_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ascent',
            name='protection',
        ),
        migrations.AddField(
            model_name='route',
            name='protection',
            field=models.CharField(choices=[('eq', 'Equipped'), ('tr', 'TRAD'), ('mx', 'Mixed')], default='eq', max_length=100),
        ),
        migrations.AddField(
            model_name='route',
            name='route_type',
            field=models.CharField(choices=[('sp', 'Single Pitch'), ('mp', 'Multi Pitch'), ('bld', 'Boulder')], default='sp', max_length=50),
        ),
        migrations.AlterField(
            model_name='route',
            name='grade',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='route',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.Place'),
        ),
        migrations.AlterField(
            model_name='route',
            name='scale',
            field=models.CharField(choices=[('yds', 'YDS'), ('fr', 'French'), ('uiaa', 'UIAA'), ('pol', 'Polish'), ('v', 'Verm')], default='fr', max_length=100),
        ),
    ]
