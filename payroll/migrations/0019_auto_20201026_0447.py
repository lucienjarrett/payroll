# Generated by Django 3.1.2 on 2020-10-26 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0018_auto_20201026_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='title',
            field=models.CharField(blank=True, choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.')], max_length=4, null=True),
        ),
    ]