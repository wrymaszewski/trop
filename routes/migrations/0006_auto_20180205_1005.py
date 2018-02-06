# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-05 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0005_auto_20180205_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='route_type',
            field=models.CharField(choices=[('Single Pitch', 'Single Pitch'), ('Multi Pitch', 'Multi Pitch'), ('Boulder', 'Boulder')], default='Single Pitch', max_length=50),
        ),
    ]
