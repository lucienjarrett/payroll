from django import VERSION
from django.core.exceptions import ValidationError
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import ManagerDescriptor
from django.urls import reverse
from django.utils import timezone
from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices
from django.core.validators import MaxValueValidator, MinValueValidator


# def validate_even(value):
#     if value % 2 != 0:
#         raise ValidationError(
#             _('%(value)s is not an even number'),
#             params={'value': value},
#         )
class Company(models.Model):
    name = models.CharField(max_length=80, verbose_name="Company Name")
    trn = models.PositiveIntegerField(verbose_name="Tax Registration #")

    class Meta:
        db_table = 'companies'
        managed = True


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
        return reverse('bank-list')


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
    image = models.ImageField(upload_to='images/', default='default.jpg')
    first_name = models.CharField(max_length=60, verbose_name="First Name")
    last_name = models.CharField(max_length=60, verbose_name="Last Name")
    GENDER = [
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
    ]
    title = models.CharField(choices=GENDER,
                             blank=True,
                             null=True,
                             max_length=4)
    nis = models.CharField(max_length=7,
                           unique=True,
                           verbose_name="National Insurance #")
    trn = models.PositiveIntegerField(unique=True,
                                      verbose_name="Tax Registration #",
                                      null=True,
                                      blank=True)
    employee_number = models.PositiveIntegerField(verbose_name="Employee #")
    date_posted = models.DateTimeField(default=timezone.now)
    rate = models.FloatField(verbose_name="Rate Of Pay",
                             validators=[MinValueValidator(0.0)],
                             null=True,
                             blank=True,
                             default=0)
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
    is_active = models.BooleanField(default=True, verbose_name='Status')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('employee-list')

    def full_name(self):
        return f'{self.first_name} { self.last_name}'

    @staticmethod
    def get_employee_id(employee_number):
        if employee_number == Employee.employee_number:
            return Employee.id

    class Meta:
        db_table = 'employees'
        managed = True
        ordering = ['employee_number']


class Salary(models.Model):
    employee = models.ForeignKey(Employee,
                                 verbose_name="Employee",
                                 on_delete=models.CASCADE)
    hours_worked = models.FloatField()
    rate = models.FloatField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.employee

    class Meta:
        db_table = 'salaries'
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if self.name == "Yoko Ono's blog":
    #         return # Yoko shall never have her own blog!
    #     else:
    #         super().save(*args, **kwargs)  # Call the "real" save() method.


class EmployeePayment(models.Model):
    employee = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE,
                                 verbose_name="Employee")
    payment = models.ForeignKey(Payment,
                                on_delete=models.CASCADE,
                                verbose_name='Other Payments')
    amount = models.FloatField(verbose_name="Payment Amount", default=0)


class Contact(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True)
    message = models.TextField()

    def __str__(self):
        """
        docstring
        """
        return f'{self.first_name} {self.last_name}'

        class Meta:
            db_table = contacts
            managed = True
