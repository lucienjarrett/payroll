# Generated by Django 3.1.2 on 2020-11-14 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0009_auto_20201114_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deduction',
            name='comment',
        ),
    ]
