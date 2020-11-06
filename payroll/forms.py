from django.db.models.fields import CharField, FloatField
from django.core import validators
from django import forms
from django.forms import TextInput, widgets
from django.forms.widgets import DateInput
from .models import (Salary, Employee, Allowance, EmployeeAllowance)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class SalaryCreateForm(forms.ModelForm):
    # hours_worked = forms.FloatField(widget=forms.TextInput(
    #     attrs={'oninput': 'calculate()'}))

    class Meta:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            helper = FormHelper()
            helper.add_input(Submit('submit', 'Save Salary'))
            helper.add_input(Submit('reset', 'Cancel'))
            helper.form_method = 'post'

        model = Salary
        fields = '__all__'
        exclude = ['date_posted']


class SalaryUpdateForm(forms.ModelForm):
    employee = forms.Select(
        attrs={
            'disabled': 'disabled',
            'placeholder': 'This is a test',
            'class': 'this is a test'
        })

    class Meta:
        model = Salary
        fields = '__all__'
        exclude = ['date_posted']


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


# class NewEmployeeForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = ()

#     allowances = forms.ModelMultipleChoiceField(
#         queryset=Allowance.objects.all())

#     def __init__(self, *args, **kwargs):
#         # Only in case we build the form from an instance
#         # (otherwise, 'toppings' list should be empty)
#         if kwargs.get('instance'):
#             # We get the 'initial' keyword argument or initialize it
#             # as a dict if it didn't exist.
#             initial = kwargs.setdefault('initial', {})
#             # The widget for a ModelMultipleChoiceField expects
#             # a list of primary key for the selected data.
#             initial['allowances'] = [
#                 t.pk for t in kwargs['instance'].allowance_set.all()
#             ]

#         forms.ModelForm.__init__(self, *args, **kwargs)

#     # Overriding save allows us to process the value of 'toppings' field
#     def save(self, commit=True):
#         # Get the unsave Pizza instance
#         instance = forms.ModelForm.save(self, False)
#         # Prepare a 'save_m2m' method for the form,
#         old_save_m2m = self.save_m2m

#         def save_m2m():
#             old_save_m2m()
#             # This is where we actually link the pizza with toppings
#             instance.allowance_set.clear()
#             instance.allowance_set.add(*self.cleaned_data['allowances'])

#         self.save_m2m = save_m2m

#         # Do we need to save all changes now?
#         if commit:
#             instance.save()
#             self.save_m2m()

#         return instance


class TimeSheetForm(forms.Form):
    employee = forms.CharField()
    date_time_from = forms.DateTimeField(widget=DateTimePicker(
        attrs={'oninput': 'calculate()'}))
    date_time_to = forms.DateTimeField(widget=DateTimePicker(
        attrs={'oninput': 'calculate()'}))
