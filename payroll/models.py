from django.utils import timezone
from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices


class Employee(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    GENDER = Choices('Male', 'Female', 'Other')
    gender = models.PositiveSmallIntegerField(choices=GENDER)
    status = StatusField(choices_name='GENDER')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'employees'
        managed = True


# class Deductions(models.Model):
#     name = models.TextField(max_length=30)
