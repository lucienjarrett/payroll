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
from collections import namedtuple
# def validate_even(value):
#     if value % 2 != 0:
#         raise ValidationError(
#             _('%(value)s is not an even number'),
#             params={'value': value},
#         )

Period = namedtuple('Period', 'Monthly Weekly Fortnightly')
PAY_PERIOD = Period(12, 48, 26)

PAY_THRESHOLD = 1500096 / PAY_PERIOD.Fortnightly
MAX_NIS = 45000 / PAY_PERIOD.Fortnightly
NHT_RATE = 0.02
ED_TAX_RATE = 0.0225
PAYE_RATE = 0.25
NIS_RATE = 0.03
SIX_MIL_PAYE = 0.30


class CommonInfo(models.Model):
    name = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        abstract = True


class Company(CommonInfo):
    name = models.CharField(max_length=80, verbose_name="Company Name")
    status = models.BooleanField(default=True, verbose_name="Status")

    class Meta:
        db_table = 'companies'
        managed = True

    def get_absolute_url(self):
        return reverse("company-list")


class Deduction(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False, verbose_name="Active?")

    # taxable = models.BooleanField(default=False)
    # comment = models.CharField(max_length=160)

    class Meta:
        db_table = "deductions"
        managed = True

    def get_absolute_url(self):
        return reverse('deduction-list')


class StatutoryDeduction(models.Model):
    name = models.CharField(max_length=100)
    rate = models.FloatField()
    max_threshold = models.FloatField()

    pass


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
    code = models.CharField(max_length=5,
                            verbose_name="Department Code",
                            unique=True)
    state = models.BooleanField(default=True, verbose_name="Is Active?")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments'
        managed = True

    def get_absolute_url(self):
        return reverse('department-list')


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
    employee_number = models.PositiveIntegerField(verbose_name="Employee #",
                                                  unique=True)
    date_posted = models.DateTimeField(default=timezone.now,
                                       blank=True,
                                       null=True)
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
    bank_account = models.CharField(verbose_name="Bank Account Number",
                                    default=None,
                                    blank=True,
                                    null=True,
                                    max_length=10)

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
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)

    # earnings = models.ManyToManyField(Earning)
    # deductions = models.ManyToManyField(Deduction)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('employee-list')

    def full_name(self):
        return f'{self.first_name} { self.last_name}'

    class Meta:
        db_table = 'employees'
        managed = True
        ordering = ['employee_number']


class Salary(models.Model):
    employee = models.ForeignKey(Employee,
                                 verbose_name="Employee",
                                 on_delete=models.CASCADE)
    hours_worked = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    date_posted = models.DateTimeField(default=timezone.now,
                                       blank=True,
                                       null=True)

    def __str__(self):
        return self.employee

    class Meta:
        db_table = 'salaries'
        managed = True
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('employee-list')

    def calculate_base_salary(self):
        return self.rate * self.hours_worked

    def calculate_nht(self):
        return self.calculate_base_salary() * NHT_RATE

    def calculate_ed_tax(self):
        #(GrossSalary – MaximumNIS) * EDTAXRate
        return (self.calculate_base_salary() -
                self.calculate_nis()) * ED_TAX_RATE

    def calculate_nis(self):
        if ((self.calculate_base_salary() * NIS_RATE) < MAX_NIS):
            return self.calculate_base_salary() * NIS_RATE
        else:
            return MAX_NIS

    def calculate_income_tax(self):
        if (self.calculate_base_salary() * 12) >= 6000000:
            print('passed')
            income_tax = (self.calculate_base_salary() - self.calculate_nis() -
                          PAY_THRESHOLD)
            return income_tax
        if ((self.calculate_base_salary() - self.calculate_nis() -
             PAY_THRESHOLD) * PAYE_RATE) > 0:
            income_tax = (self.calculate_base_salary() - self.calculate_nis())
            return income_tax
        else:
            return 0

    def calculate_other_deductions(self):
        return 0

    def calculate_net_pay(self):
        print(
            f'{self.calculate_nht()} - {self.calculate_ed_tax()} - {self.calculate_income_tax()}'
        )
        net_pay = self.calculate_base_salary() - (
            self.calculate_nht() + self.calculate_ed_tax() +
            self.calculate_nis() + self.calculate_income_tax())
        return net_pay


# class EmployeePayment(models.Model):
#     employee = models.ForeignKey(Employee,
#                                  on_delete=models.CASCADE,
#                                  verbose_name="Employee")
#     payment = models.ForeignKey(Earning,
#                                 on_delete=models.CASCADE,
#                                 verbose_name='Other Payments')
#     amount = models.FloatField(verbose_name="Payment Amount", default=0)


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


class Earning(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name='Earnings',
                            unique=True)
    taxable = models.BooleanField(default=False, verbose_name="Is taxable?")

    # employees = models.ManyToManyField(Employee,
    #                                    through='EmployeeEarning',
    #                                    through_fields=("earning", "employee"))
    def __str__(self):
        return self.name

    class Meta:
        db_table = "earning"
        managed = True

    def get_absolute_url(self):
        return reverse('earning-list')


class EmployeeEarning(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    earning = models.ForeignKey(Earning, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.employee.first_name} {self.earning.name}'
