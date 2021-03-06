# Generated by Django 3.1.2 on 2020-12-22 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0049_auto_20201220_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheetdetail',
            name='date_time_in',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='timesheetdetail',
            name='date_time_out',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='timesheetdetail',
            name='hours',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
