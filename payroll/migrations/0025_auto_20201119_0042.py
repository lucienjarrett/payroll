# Generated by Django 3.1.2 on 2020-11-19 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0024_employee_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='address1',
            field=models.CharField(blank=True, default=None, max_length=160, null=True, verbose_name='Street Address 1'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address2',
            field=models.CharField(blank=True, default=None, max_length=160, null=True, verbose_name='Street Address 2'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]