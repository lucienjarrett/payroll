# Generated by Django 3.1.2 on 2020-11-01 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0037_employee_allowances'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='allowances',
            field=models.ManyToManyField(related_name='employees', to='payroll.Allowance'),
        ),
    ]
