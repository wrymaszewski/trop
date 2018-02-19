# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-17 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indoor', '0005_auto_20180211_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='top',
            name='grade_bld_fr',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='top',
            name='grade_fr',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='top',
            name='grade',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='top',
            name='scale',
            field=models.CharField(choices=[('YDS', 'YDS'), ('FR', 'French'), ('UIAA', 'UIAA'), ('POL', 'Polish'), ('V', 'Vermin')], default='FR', max_length=100),
        ),
    ]