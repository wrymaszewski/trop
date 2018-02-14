# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-12 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0018_remove_place_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='slugs', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='slugs', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
