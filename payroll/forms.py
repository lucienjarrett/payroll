from django.db.models.fields import CharField, FloatField
from django.core import validators
from django import forms
from django.forms import TextInput, widgets
from django.forms.widgets import DateInput
from .models import Earning, EmployeeEarning, Salary, Employee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class SalaryCreateForm(forms.ModelForm):
    hours_worked = forms.FloatField(widget=forms.TextInput(
        attrs={'oninput': 'calculate()'}))
    holiday_pay = forms.FloatField(widget=forms.TextInput(
        attrs={'oninput': 'calculate()'}))
    submit = Submit('submit', 'Save Salary')

    class Meta:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            helper = FormHelper()
            helper.add_input(Submit('submit', 'Save Salary'))
            helper.add_input(Submit('reset', 'Cancel'))
            helper.form_method = 'post'

        model = Salary
        # fields = ['employee', 'hours_worked', 'salary']
        fields = '__all__'


class EmployeeCreateForm(forms.ModelForm):
    title = forms.Select()
    first_name = forms.CharField(label="First Name",
                                 widget=forms.TextInput(),
                                 required=True)
    last_name = forms.CharField(label="Last Name",
                                widget=forms.TextInput(),
                                required=True)
    employee_number = forms.CharField(
        label="Employee #",
        required=True,
        widget=forms.TextInput(attrs={'type': 'number'}))
    nis = forms.CharField(label="National Insurance #",
                          required=True,
                          widget=forms.TextInput())
    trn = forms.CharField(label="Tax Registration #",
                          required=True,
                          widget=forms.TextInput(attrs={'type': 'number'}))

    job_title = forms.Select()
    department = forms.Select()
    payment = forms.Select(attrs={'onchange': 'check_for_bank()'})
    bank = forms.Select()
    bank_account = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'type': 'text'}))
    payment_schedule = forms.Select()
    basic_pay = forms.CharField(required=False,
                                label="Base Pay",
                                widget=forms.TextInput(attrs={
                                    'type': 'number',
                                    'min': 0,
                                    'step': 0.01
                                }))
    employment_date = forms.DateField(required=False, widget=DatePicker())
    departure_date = forms.DateField(required=False, widget=DatePicker())
    is_active = forms.BooleanField(required=False, label='Active?')
    rate = forms.FloatField(required=False,
                            widget=forms.TextInput(attrs={
                                'type': 'number',
                                'min': 0,
                                'step': 0.01
                            }))

    class Meta:
        model = Employee
        fields = (
            'title',
            'first_name',
            'last_name',
            'trn',
            'nis',
            'employee_number',
            'job_title',
            'department',
            'payment',
            'bank',
            'bank_account',
            'payment_schedule',
            'basic_pay',
            'employment_date',
            'departure_date',
            'is_active',
            'rate',
        )


class EmployeeBenefitsForm(forms.ModelForm):
    class Meta:
        model = EmployeeEarning
        fields = ['employee', 'earning']
