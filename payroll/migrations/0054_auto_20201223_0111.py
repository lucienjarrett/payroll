# Generated by Django 3.1.2 on 2020-12-23 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0053_auto_20201222_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheetdetail',
            name='hours',
            field=models.FloatField(verbose_name='Work hours.'),
        ),
    ]
