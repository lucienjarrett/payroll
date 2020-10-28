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

