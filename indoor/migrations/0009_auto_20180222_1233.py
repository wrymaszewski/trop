# Generated by Django 2.0.2 on 2018-02-22 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indoor', '0008_auto_20180222_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='top',
            name='route_type',
            field=models.CharField(choices=[('BLD', 'Boulder'), ('R', 'Rope')], default='R', max_length=100, verbose_name='Type'),
        ),
    ]
