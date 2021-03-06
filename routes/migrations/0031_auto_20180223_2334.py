# Generated by Django 2.0.2 on 2018-02-23 23:34

from django.db import migrations, models
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0030_auto_20180223_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sector',
            name='location',
            field=location_field.models.plain.PlainLocationField(default='37.6564706,-119.5724832', max_length=63),
        ),
        migrations.AlterField(
            model_name='sector',
            name='region',
            field=models.CharField(max_length=250, verbose_name='Region, Country'),
        ),
    ]
