# Generated by Django 3.1.2 on 2020-11-16 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0017_auto_20201116_0404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deduction',
            name='ded_bef_or_after',
        ),
    ]
