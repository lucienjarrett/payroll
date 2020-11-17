# Generated by Django 3.1.2 on 2020-11-17 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0018_remove_deduction_ded_bef_or_after'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=120)),
                ('address_1', models.CharField(max_length=120)),
                ('address_2', models.CharField(max_length=120)),
                ('parish', models.PositiveSmallIntegerField(choices=[(1, 'Clarendon'), (2, 'Manchester'), (3, 'St. Catherine'), (4, 'Portland'), (5, 'St. Ann'), (6, 'Kingston'), (7, 'St. Elizabeth'), (8, 'Westmoreland'), (9, 'St. James'), (10, 'Hanover'), (11, 'Trelawny'), (12, 'St. Mary'), (13, 'St. Andrew'), (14, 'St. Thomas')])),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='deduction',
            old_name='status',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='state',
            new_name='is_active',
        ),
        migrations.RemoveField(
            model_name='allowance',
            name='date_posted',
        ),
        migrations.AddField(
            model_name='allowance',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='leavetype',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='leavetype',
            name='leave_day',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leavetype',
            name='name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
