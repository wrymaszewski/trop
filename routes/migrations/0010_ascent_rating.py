# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-05 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0009_auto_20180205_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='ascent',
            name='rating',
            field=models.IntegerField(choices=[(0, 'Low'), (1, 'Medium'), (2, 'High')], default=1),
        ),
    ]