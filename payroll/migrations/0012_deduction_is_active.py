# Generated by Django 3.1.2 on 2020-11-14 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0011_remove_deduction_taxable'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
