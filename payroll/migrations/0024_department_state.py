# Generated by Django 3.1.2 on 2020-10-29 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0023_auto_20201029_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]