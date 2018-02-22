# Generated by Django 2.0.2 on 2018-02-22 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indoor', '0007_auto_20180221_1346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='top',
            old_name='grade_bld_fr',
            new_name='grade_converted',
        ),
        migrations.RemoveField(
            model_name='top',
            name='grade_fr',
        ),
        migrations.AlterField(
            model_name='top',
            name='ascent_style',
            field=models.CharField(choices=[('OS', 'OS'), ('FL', 'Flash'), ('RP', 'RP'), ('PP', 'PP'), ('AF', 'AF'), ('TR', 'TR')], default='OS', max_length=100, verbose_name='Style'),
        ),
    ]
