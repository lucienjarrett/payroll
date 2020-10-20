from django.db import models


class Employee(models.Model):
    first_name = models.TextField(max_length=60)
    last_name = models.TextField(max_length=60)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Deductions(models.Model):
    name = models.TextField(max_length=30)
