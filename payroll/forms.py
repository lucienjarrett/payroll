from django.db.models.fields import CharField, FloatField
from django.core import validators
from django import forms
from django.forms import TextInput, widgets
from .models import Salary, Employee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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
    employee_number = forms.CharField(label="Employee #",
                                      required=True,
                                      widget=forms.TextInput())
    nis = forms.CharField(label="National Insurance #",
                          required=True,
                          widget=forms.TextInput())
    trn = forms.CharField(label="Tax Registration #",
                          required=True,
                          widget=forms.TextInput())

    job_title = forms.Select()
    department = forms.Select()

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
        )
