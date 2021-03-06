# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-04 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ascent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('ascent_style', models.CharField(choices=[('os', 'OS'), ('fl', 'Flash'), ('rp', 'RP'), ('pp', 'PP'), ('af', 'AF'), ('tr', 'TR')], max_length=20)),
                ('protection', models.CharField(choices=[('eq', 'Equipped'), ('tr', 'TRAD'), ('mx', 'Mixed')], max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('location', location_field.models.plain.PlainLocationField(max_length=63)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=10)),
                ('scale', models.CharField(choices=[('yds', 'YDS'), ('fr', 'French'), ('uiaa', 'UIAA'), ('pol', 'Polish'), ('v', 'Verm')], max_length=20)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.Place')),
            ],
        ),
        migrations.AddField(
            model_name='ascent',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.Route'),
        ),
        migrations.AddField(
            model_name='ascent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User'),
        ),
    ]
