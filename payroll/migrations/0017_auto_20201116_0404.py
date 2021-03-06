# Generated by Django 3.1.2 on 2020-11-16 04:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0016_auto_20201115_2256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'managed': True, 'ordering': ['-employee_number']},
        ),
        migrations.RemoveField(
            model_name='employee',
            name='date_posted',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='date_posted',
        ),
        migrations.AlterField(
            model_name='employee',
            name='basic_pay',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Basic Pay'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='nis',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.MinLengthValidator(7)], verbose_name='National Insurance #'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='trn',
            field=models.PositiveIntegerField(default=111111111, unique=True, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)], verbose_name='Tax Registration #'),
            preserve_default=False,
        ),
    ]
