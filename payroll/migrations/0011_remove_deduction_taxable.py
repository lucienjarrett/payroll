# Generated by Django 3.1.2 on 2020-11-14 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0010_remove_deduction_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deduction',
            name='taxable',
        ),
    ]