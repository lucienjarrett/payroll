# Generated by Django 3.1.2 on 2020-10-22 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0013_auto_20201022_0405'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='total_salary',
            field=models.FloatField(default=0),
        ),
    ]