# Generated by Django 3.1.2 on 2020-11-03 22:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allowance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Allowances')),
                ('taxable', models.BooleanField(default=False, verbose_name='Is taxable?')),
            ],
            options={
                'db_table': 'allowance',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Bank name')),
                ('short_code', models.CharField(max_length=10, verbose_name='Short code')),
            ],
            options={
                'db_table': 'banks',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Company Name')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            options={
                'db_table': 'companies',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=254)),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('message', models.TextField()),
            ],
            options={
                'db_table': 'contacts',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Deduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False, verbose_name='Active?')),
            ],
            options={
                'db_table': 'deductions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Department Name')),
                ('code', models.CharField(max_length=5, unique=True, verbose_name='Department Code')),
                ('state', models.BooleanField(default=True, verbose_name='Is Active?')),
            ],
            options={
                'db_table': 'departments',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DutyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Duty Type Name')),
            ],
            options={
                'db_table': 'duty_types',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='images/')),
                ('first_name', models.CharField(max_length=60, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=60, verbose_name='Last Name')),
                ('title', models.CharField(blank=True, choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.')], max_length=4, null=True)),
                ('nis', models.CharField(max_length=7, unique=True, verbose_name='National Insurance #')),
                ('trn', models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='Tax Registration #')),
                ('employee_number', models.PositiveIntegerField(unique=True, verbose_name='Employee #')),
                ('date_posted', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('rate', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Rate Of Pay')),
                ('bank_account', models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Bank Account Number')),
                ('basic_pay', models.FloatField(blank=True, default=0, null=True, verbose_name='Basic Pay')),
                ('employment_date', models.DateField(blank=True, default=None, null=True, verbose_name='Employment Date')),
                ('departure_date', models.DateField(blank=True, default=None, null=True, verbose_name='Departure Date')),
                ('is_active', models.BooleanField(default=True, verbose_name='Status')),
            ],
            options={
                'db_table': 'employees',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Job title')),
            ],
            options={
                'db_table': 'job_titles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Payment Method')),
            ],
            options={
                'db_table': 'payment_methods',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PayPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Pay Period')),
            ],
            options={
                'db_table': 'pay_period',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StatutoryDeduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rate', models.FloatField()),
                ('max_threshold', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_worked', models.FloatField(default=0)),
                ('rate', models.FloatField(default=0)),
                ('date_posted', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.employee', verbose_name='Employee')),
            ],
            options={
                'db_table': 'salaries',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EmployeeAllowance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_recurring', models.BooleanField(default=False)),
                ('date_from', models.DateField(blank=True, null=True)),
                ('date_to', models.DateField(blank=True, null=True)),
                ('allowance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_allowances', to='payroll.allowance')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_allowances', to='payroll.employee')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='allowances',
            field=models.ManyToManyField(related_name='employees', through='payroll.EmployeeAllowance', to='payroll.Allowance'),
        ),
        migrations.AddField(
            model_name='employee',
            name='bank',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='payroll.bank', verbose_name='Banks With'),
        ),
        migrations.AddField(
            model_name='employee',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='payroll.company'),
        ),
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='payroll.department'),
        ),
        migrations.AddField(
            model_name='employee',
            name='job_title',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='payroll.jobtitle', verbose_name='Job Title'),
        ),
        migrations.AddField(
            model_name='employee',
            name='payment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='payroll.paymentmethod', verbose_name='Pay By'),
        ),
        migrations.AddField(
            model_name='employee',
            name='payment_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='payroll.payperiod', verbose_name='Pay Cycle'),
        ),
    ]
