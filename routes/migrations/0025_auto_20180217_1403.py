# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-17 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0024_auto_20180217_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='grade_bld_fr',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='grade_bld_v',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]