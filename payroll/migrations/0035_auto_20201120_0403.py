# Generated by Django 3.1.2 on 2020-11-20 04:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import payroll.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payroll', '0034_auto_20201120_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='company',
            name='national_ins_num',
            field=models.CharField(default=11111, max_length=8, unique=True, validators=[payroll.validators.nis_validator]),
        ),
        migrations.AlterField(
            model_name='company',
            name='tax_reg_num',
            field=models.IntegerField(validators=[payroll.validators.trn_validator]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='parish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.parish'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='trn',
            field=models.PositiveIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999), payroll.validators.trn_validator], verbose_name='Tax Registration #'),
        ),
        migrations.AlterField(
            model_name='parish',
            name='name',
            field=models.CharField(default=None, max_length=120, unique=True),
        ),
    ]
