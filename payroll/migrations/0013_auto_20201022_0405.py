# Generated by Django 3.1.2 on 2020-10-22 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0012_salary_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherDeduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StatutoryDeduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='salary',
            name='holiday_pay',
            field=models.FloatField(default=0),
        ),
    ]
