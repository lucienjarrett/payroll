# Generated by Django 3.1.2 on 2020-10-21 22:56

from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0008_employee_bank_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='gender',
        ),
        migrations.AddField(
            model_name='employee',
            name='title',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='----', max_length=100, no_check_for_status=True),
        ),
    ]
