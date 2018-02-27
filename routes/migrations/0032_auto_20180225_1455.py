# Generated by Django 2.0.2 on 2018-02-25 14:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0031_auto_20180223_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sector',
            name='region',
            field=models.CharField(max_length=250, validators=[django.core.validators.RegexValidator(message='Input needs to consist of region and country names divided by a comma (,) and a space', regex='.+,\\s.+')], verbose_name='Region, Country'),
        ),
    ]