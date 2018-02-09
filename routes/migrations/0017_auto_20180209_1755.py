# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-09 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0016_auto_20180209_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='city',
            field=models.CharField(max_length=100, verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='route',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='routes.Place', verbose_name='Crag'),
        ),
    ]
