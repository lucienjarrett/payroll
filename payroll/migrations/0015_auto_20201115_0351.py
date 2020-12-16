# Generated by Django 3.1.2 on 2020-11-15 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0014_deduction_ded_bef_or_after'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'managed': True, 'ordering': ['employee_number']},
        ),
        migrations.AlterField(
            model_name='deduction',
            name='employer_rate',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='deduction',
            name='max_for_year',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='basic_pay',
            field=models.FloatField(default=0, verbose_name='Basic Pay'),
        ),
    ]