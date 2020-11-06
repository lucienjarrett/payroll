# Generated by Django 3.1.2 on 2020-11-05 21:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeDeduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('pay_period', models.DateField()),
                ('date_posted', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='employee',
            name='allowances',
        ),
        migrations.RemoveField(
            model_name='employeeallowance',
            name='date_from',
        ),
        migrations.RemoveField(
            model_name='employeeallowance',
            name='date_to',
        ),
        migrations.RemoveField(
            model_name='employeeallowance',
            name='is_recurring',
        ),
        migrations.AddField(
            model_name='allowance',
            name='comment',
            field=models.CharField(default=None, max_length=160),
        ),
        migrations.AddField(
            model_name='allowance',
            name='date_posted',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='deduction',
            name='comment',
            field=models.CharField(default=None, max_length=160),
        ),
        migrations.AddField(
            model_name='deduction',
            name='date_posted',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='deduction',
            name='taxable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeeallowance',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='employeeallowance',
            name='date_posted',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='employeeallowance',
            name='pay_period',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='employee',
            name='payment_schedule',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Weekly'), (2, 'Forthnightly'), (3, 'Monthly')], null=True),
        ),
        migrations.AlterField(
            model_name='employeeallowance',
            name='allowance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payroll.allowance'),
        ),
        migrations.AlterField(
            model_name='employeeallowance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.employee'),
        ),
        migrations.DeleteModel(
            name='PayPeriod',
        ),
        migrations.AddField(
            model_name='employeededuction',
            name='allowance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payroll.allowance'),
        ),
        migrations.AddField(
            model_name='employeededuction',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.employee'),
        ),
    ]
