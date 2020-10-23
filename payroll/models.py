from django import VERSION
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import ManagerDescriptor
from django.urls import reverse
from django.utils import timezone
from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices
from django.core.validators import MaxValueValidator, MinValueValidator


class Payment(models.Model):
    name = models.CharField(max_length=30, verbose_name='Taxable Payments')
    taxable = models.BooleanField(default=False, verbose_name="Is taxable?")

    class Meta:
        db_table = "payments"
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class OtherDeduction(models.Model):
    class Meta:
        db_table = "other_deduction"
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class PayPeriod(models.Model):
    name = models.CharField(verbose_name="Pay Period", max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "pay_period"
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class DutyType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Duty Type Name")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "duty_types"
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, verbose_name='Payment Method')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "payment_methods"
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class Bank(models.Model):
    name = models.CharField(max_length=100, verbose_name='Bank name')
    short_code = models.CharField(max_length=10, verbose_name="Short code")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "banks"
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class Department(models.Model):
    name = models.CharField(max_length=30, verbose_name="Department Name")
    code = CharField(max_length=5, verbose_name="Department Code")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments'
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class JobTitle(models.Model):
    name = models.CharField(max_length=60, verbose_name="Job title")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'job_titles'
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class Employee(models.Model):
    # image = models.ImageField(upload_to='images/')
    first_name = models.CharField(max_length=60, verbose_name="First Name")
    last_name = models.CharField(max_length=60, verbose_name="Last Name")
    GENDER = Choices('----', 'Mr.', 'Ms.')
    title = StatusField(choices_name='GENDER')
    nis = models.CharField(max_length=7,
                           unique=True,
                           verbose_name="National Insurance #")
    trn = models.PositiveIntegerField(unique=True,
                                      verbose_name="Tax Registration #")
    employee_number = models.PositiveIntegerField(verbose_name="Employee #")
    date_posted = models.DateTimeField(default=timezone.now)
    rate = models.FloatField(verbose_name="Rate Of Pay",
                             validators=[MinValueValidator(0.0)])
    department = models.ForeignKey(Department,
                                   on_delete=models.CASCADE,
                                   default=None,
                                   null=True,
                                   blank=True)
    job_title = models.ForeignKey(JobTitle,
                                  verbose_name="Job Title",
                                  on_delete=models.CASCADE,
                                  default=None,
                                  null=True,
                                  blank=True)

    payment = models.ForeignKey(
        PaymentMethod,
        verbose_name="Pay By",
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    bank = models.ForeignKey(Bank,
                             verbose_name="Banks With",
                             on_delete=models.CASCADE,
                             default=None,
                             blank=True,
                             null=True)
    bank_account = models.PositiveIntegerField(
        verbose_name="Bank Account Number", blank=True, null=True)

    payment_schedule = models.ForeignKey(PayPeriod,
                                         on_delete=models.CASCADE,
                                         blank=True,
                                         null=True,
                                         verbose_name="Pay Cycle")
    basic_pay = models.FloatField(
        verbose_name="Basic Pay",
        default=0,
        null=True,
        blank=True,
    )
    employment_date = models.DateField(verbose_name="Employment Date",
                                       null=True,
                                       blank=True,
                                       default=None)
    departure_date = models.DateField(verbose_name="Departure Date",
                                      null=True,
                                      blank=True,
                                      default=None)
    CLASSIFICATION = [
        ("", '-------'),
        (1, 'Salaried'),
        (2, 'Hourly'),
        (3, 'Commissioned'),
    ]
    classification = models.CharField(max_length=1,
                                      choices=CLASSIFICATION,
                                      default=2,
                                      blank=0,
                                      null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('employee-list')

    class Meta:
        db_table = 'employees'
        managed = True


class Salary(models.Model):
    employee = models.ForeignKey(Employee,
                                 verbose_name="Employee",
                                 on_delete=models.CASCADE)
    hours_worked = models.FloatField()
    date_posted = models.DateTimeField(default=timezone.now)
    salary = models.FloatField(default=0)
    holiday_pay = models.FloatField(default=0)
    total_salary = models.FloatField(default=0)

    def __str__(self):
        return self.employee

    class Meta:
        db_table = 'salaries'
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class EmployeePayment(models.Model):
    employee = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE,
                                 verbose_name="Employee")
    payment = models.ForeignKey(Payment,
                                on_delete=models.CASCADE,
                                verbose_name='Other Payments')
    amount = models.FloatField(verbose_name="Payment Amount", default=0)
