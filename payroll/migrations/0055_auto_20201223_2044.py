# Generated by Django 3.1.2 on 2020-12-23 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0054_auto_20201223_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheetdetail',
            name='hours',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Work hours.'),
        ),
    ]
