# Generated by Django 3.1.2 on 2020-11-30 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payroll', '0040_auto_20201129_2218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'managed': True, 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'managed': True, 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='employeeallowance',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='parish',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'managed': True},
        ),
        migrations.AlterField(
            model_name='employee',
            name='country',
            field=models.CharField(blank=True, default='Jamaica', max_length=160),
        ),
        migrations.AlterField(
            model_name='employee',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='timesheetdetail',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='payroll.employee'),
        ),
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_from', models.DateField(blank=True, default=None, null=True)),
                ('date_to', models.DateField(blank=True, default=None, null=True)),
                ('comment', models.TextField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employeeleave_created_by', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='payroll.employee')),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves_types', to='payroll.leavetype')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employeeleave_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
            },
        ),
    ]