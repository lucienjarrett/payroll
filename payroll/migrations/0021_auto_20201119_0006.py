# Generated by Django 3.1.2 on 2020-11-19 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0020_auto_20201118_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='address1',
            field=models.CharField(default=1, max_length=160),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='address2',
            field=models.CharField(default='Address2', max_length=160),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='city_parish',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Clarendon'), (2, 'Manchester'), (3, 'St. Catherine'), (4, 'Portland'), (5, 'St. Ann'), (6, 'Kingston'), (7, 'St. Elizabeth'), (8, 'Westmoreland'), (9, 'St. James'), (10, 'Hanover'), (11, 'Trelawny'), (12, 'St. Mary'), (13, 'St. Andrew'), (14, 'St. Thomas')], default=1, verbose_name='City/Parish'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='country',
            field=models.CharField(default='Jamaica', max_length=160),
        ),
    ]