# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-17 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0022_auto_20180217_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='grade_bld_fr',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='route',
            name='grade_bld_v',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='route',
            name='grade_fr',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='route',
            name='grade_pol',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='route',
            name='grade_uiaa',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='route',
            name='grade_yds',
            field=models.CharField(max_length=20),
        ),
    ]
