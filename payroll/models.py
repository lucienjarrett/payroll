from django.core.exceptions import ValidationError
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse
from django.urls.base import translate_url
from django.utils import timezone
from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices
from django.core.validators import MaxValueValidator, MinValueValidator
from collections import namedtuple
from django.utils.text import slugify
from django.contrib.auth.models import User
from .validators import nis_validator, trn_validator
from django.core import validators
from django.core.exceptions import ValidationError


class CommonInfo(models.Model):
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   blank=True,
                                   null=True)

    class Meta:
        abstract = True


class Parish(CommonInfo):
    name = models.CharField(max_length=120, default=None, unique=True)

    def __str__(self):
        return self.name


class Company(CommonInfo):
    name = models.CharField(max_length=80, verbose_name="Company Name")
    status = models.BooleanField(default=True, verbose_name="Status")
    national_ins_num = models.CharField(max_length=8,
                                        unique=True,
                                        default=11111,
                                        validators=[nis_validator])
    tax_reg_num = models.IntegerField(validators=[trn_validator])

    class Meta:
        #db_table = 'companies'
        managed = True

    def get_absolute_url(self):
        return reverse("company-list")


class Customer(CommonInfo):
    name = models.CharField(max_length=120)
    address_1 = models.CharField(max_length=120)
    address_2 = models.CharField(max_length=120)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Deduction(CommonInfo):
    # TAX_APPLIED = [(1, 'Before'), (2, 'After')]
    name = models.CharField(max_length=100)
    short_code = models.CharField(max_length=25, unique=True)
    short_description = models.CharField(max_length=50)
    is_statutory = models.BooleanField(default=False)
    employee_rate = models.DecimalField(default=0,
                                        max_digits=8,
                                        decimal_places=3)
    employer_rate = models.DecimalField(default=0,
                                        max_digits=8,
                                        decimal_places=3)
    is_active = models.BooleanField(default=False, verbose_name="Active?")
    max_for_year = models.DecimalField(default=0,
                                       decimal_places=3,
                                       max_digits=15,
                                       null=True,
                                       blank=True)

    class Meta:
        #db_table = "deductions"
        managed = True

    def get_absolute_url(self):
        return reverse('deduction-list')


class DutyType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Duty Type Name")

    def __str__(self):
        return self.name

    class Meta:
        #db_table = "duty_types"
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class PaymentMethod(CommonInfo):
    name = models.CharField(max_length=50, verbose_name='Payment Method')

    def __str__(self):
        return self.name

    class Meta:
        #db_table = "payment_methods"
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class Bank(CommonInfo):
    name = models.CharField(max_length=100, verbose_name='Bank name')
    short_code = models.CharField(max_length=10, verbose_name="Short code")
    transit_no = models.PositiveIntegerField(default=None,
                                             blank=True,
                                             null=True)

    def __str__(self):
        return self.name

    class Meta:
        #db_table = "banks"
        managed = True

    def get_absolute_url(self):
        return reverse('bank-list')


class Department(CommonInfo):
    name = models.CharField(max_length=30, verbose_name="Department Name")
    code = models.CharField(max_length=5,
                            verbose_name="Department Code",
                            unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __str__(self):
        return self.name

    class Meta:
        #db_table = 'departments'
        managed = True

    def get_absolute_url(self):
        return reverse('department-list')


class JobTitle(CommonInfo):
    name = models.CharField(max_length=60, verbose_name="Job title")

    def __str__(self):
        return self.name

    class Meta:
        #db_table = 'job_titles'
        managed = True

    def get_absolute_url(self):
        return reverse('employee-list')


class Employee(CommonInfo):
    image = models.ImageField(upload_to='images/', default='default.jpg')
    first_name = models.CharField(max_length=60, verbose_name="First Name")
    last_name = models.CharField(max_length=60, verbose_name="Last Name")
    middle_name = models.CharField(max_length=60,
                                   verbose_name="Middle Name",
                                   default="",
                                   blank=True,
                                   null=True)

    address1 = models.CharField(max_length=160,
                                default=None,
                                null=True,
                                blank=True,
                                verbose_name="Street Address 1")
    address2 = models.CharField(max_length=160,
                                default=None,
                                null=True,
                                blank=True,
                                verbose_name="Street Address 2")

    city_parish = models.ForeignKey(Parish,
                                    on_delete=Parish,
                                    verbose_name='City/Parish',
                                    default=None,
                                    null=True,
                                    blank=True)

    country = models.CharField(max_length=160,
                               default="Jamaica",
                               null=True,
                               blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER = [
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
        ('Mrs.', 'Mrs.'),
    ]

    PAY_PRD = [
        (1, 'Weekly'),
        (2, 'Forthnightly'),
        (3, 'Monthly'),
    ]
    title = models.CharField(choices=GENDER,
                             blank=True,
                             null=True,
                             max_length=4)
    nis = models.CharField(validators=[
        nis_validator,
    ],
                           max_length=7,
                           unique=True,
                           verbose_name="National Insurance #")
    trn = models.PositiveIntegerField(unique=True,
                                      verbose_name="Tax Registration #",
                                      validators=[
                                          MinValueValidator(100000000),
                                          MaxValueValidator(999999999),
                                          trn_validator
                                      ])

    employee_number = models.PositiveIntegerField(verbose_name="Employee #",
                                                  unique=True)
    rate = models.FloatField(verbose_name="Rate Of Pay",
                             validators=[MinValueValidator(0.0)],
                             null=True,
                             blank=True,
                             default=0)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name="employees",
    )
    job_title = models.ForeignKey(JobTitle,
                                  related_name="employees",
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
        related_name="employees",
    )
    bank = models.ForeignKey(
        Bank,
        verbose_name="Banks With",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        related_name="employees",
    )
    GNDR = [
        (1, 'Male'),
        (2, 'Female'),
    ]
    gender = models.PositiveSmallIntegerField(choices=GNDR,
                                              default=1,
                                              blank=True,
                                              null=True)
    phone = models.CharField(max_length=10,
                             blank=True,
                             null=True,
                             verbose_name="Home Phone:")
    alternate_phone = models.CharField(max_length=10,
                                       blank=True,
                                       null=True,
                                       verbose_name='Mobile')
    work_phone = models.CharField(max_length=10,
                                  blank=True,
                                  null=True,
                                  verbose_name='Work Phone')
    email = models.EmailField(
        blank=True,
        null=True,
    )
    bank_account = models.CharField(verbose_name="Bank Account Number",
                                    default=None,
                                    blank=True,
                                    null=True,
                                    max_length=10)
    payment_schedule = models.PositiveIntegerField(choices=PAY_PRD,
                                                   blank=True,
                                                   null=True)
    basic_pay = models.FloatField(verbose_name="Basic Pay",
                                  default=0,
                                  validators=[MinValueValidator(0.0)])

    employment_date = models.DateField(verbose_name="Employment Date",
                                       null=True,
                                       blank=True,
                                       default=None)
    departure_date = models.DateField(verbose_name="Departure Date",
                                      null=True,
                                      blank=True,
                                      default=None)
    is_active = models.BooleanField(default=True, verbose_name='Status')
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="employees",
    )

    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   blank=True,
                                   null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('employee-list')

    def full_name(self):
        return f'{self.first_name} { self.last_name}'

    class Meta:
        db_table = 'employees'
        managed = True
        ordering = ['-employee_number']


class Salary(CommonInfo):
    PAY_THRESHOLD = 1500096
    MAX_NIS = 45000
    NHT_RATE = 0.02
    ED_TAX_RATE = 0.0225
    PAYE_RATE = 0.25
    NIS_RATE = 0.03
    SIX_MIL_PAYE = 0.30

    employee = models.ForeignKey(Employee,
                                 verbose_name="Employee",
                                 on_delete=models.CASCADE)
    hours_worked = models.FloatField(default=0)
    rate = models.FloatField(default=0)

    class Meta:
        #db_table = 'salaries'
        managed = True
        ordering = ['id']

    def get_pay_schedule(self):
        if self.employee.payment_schedule:
            return self.employee.payment_schedule
        else:
            return 2  #Fortnightly for now.

    def __str__(self):
        return "1"

    def get_pay_schedule_vals(self):
        if self.get_pay_schedule() == 1:
            return 48
        elif self.get_pay_schedule() == 2:
            return 26
        elif self.get_pay_schedule() == 3:
            return 12

    def pay_thresold(self):
        threshold = self.PAY_THRESHOLD / self.get_pay_schedule_vals()
        return threshold

    def max_nis(self):
        nis = self.MAX_NIS / self.get_pay_schedule_vals()
        return nis

    def get_absolute_url(self):
        return reverse('salary-list')

    def calculate_base_salary(self):
        if self.rate <= 0:
            return self.employee.rate * self.hours_worked
        else:
            return self.rate * self.hours_worked

    def calculate_nht(self):
        return self.calculate_base_salary() * self.NHT_RATE

    def calculate_ed_tax(self):
        return (self.calculate_base_salary() -
                self.calculate_nis()) * self.ED_TAX_RATE

    def calculate_nis(self):
        if ((self.calculate_base_salary() * self.NIS_RATE) < self.max_nis()):
            return self.calculate_base_salary() * self.NIS_RATE
        else:
            return self.max_nis()

    def calculate_income_tax(self):
        if (self.calculate_base_salary() * 12) >= 6000000:
            income_tax = (self.calculate_base_salary() - self.calculate_nis() -
                          self.pay_thresold())
            return income_tax
        if ((self.calculate_base_salary() - self.calculate_nis() -
             self.pay_thresold()) * self.PAYE_RATE) > 0:
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


class Contact(CommonInfo):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True)
    message = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        # db_table = "contacts"
        managed = True


class Allowance(CommonInfo):
    name = models.CharField(max_length=30,
                            verbose_name='Allowances',
                            unique=True)
    taxable = models.BooleanField(default=False, verbose_name="Is taxable?")
    comment = models.CharField(max_length=160, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        # db_table = "allowance"
        managed = True

    def get_absolute_url(self):
        return reverse('allowance-list')


class EmployeeAllowance(CommonInfo):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    allowance = models.ForeignKey(Allowance,
                                  on_delete=models.CASCADE,
                                  null=True)
    amount = models.FloatField(default=0)
    pay_period = models.DateField(default=None)

    def __str__(self):
        return f'{self.employee.first_name} {self.allowance.name}'


class TimesheetHeader(models.Model):
    customer = models.CharField(verbose_name='Customer',
                                blank=True,
                                null=True,
                                max_length=100,
                                default=None)

    class Meta:
        # db_table = 'time_sheet_header'
        managed = True


class TimeSheetDetail(models.Model):
    # employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_sheet_header = models.ForeignKey(TimesheetHeader,
                                          related_name="time_sheet_header",
                                          on_delete=models.CASCADE,
                                          default=None)
    employee = models.ForeignKey(Employee,
                                 related_name="employees",
                                 on_delete=models.CASCADE)

    date_time_in = models.DateTimeField(default=None, blank=True, null=True)
    date_time_out = models.DateTimeField(default=None, blank=True, null=True)
    hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        # db_table = 'time_sheet_detail'
        managed = True


class LeaveType(CommonInfo):
    name = models.CharField(max_length=150)
    leave_day = models.SmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    # INSERT INTO `leave_types` (`type_id`, `name`, `leave_day`, `status`) VALUES
    # (1, 'Casual Leave', '21', 1),
    # (2, 'Sick Leave', '15', 1),
    # (3, 'Maternity Leave', '90', 1),
    # (4, 'Paternal Leave', '7', 1),
    # (5, 'Earned leave', '', 1),
    # (7, 'Public Holiday', '', 1),
    # (8, 'Optional Leave', '', 1),
    # (9, 'Leave without Pay', '', 1);


class Report(CommonInfo):
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField()
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('employee-list')


#payroll run date, check_date