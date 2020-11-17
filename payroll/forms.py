from django.db.models.fields import CharField, FloatField
from django.core import validators
from django import forms
from django.forms import TextInput, widgets
from django.forms.widgets import DateInput
from .models import (Deduction, Salary, Employee, Allowance, EmployeeAllowance)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Fieldset
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

nis_validator = validators.RegexValidator(r"[A-Z]{1}\d{6}$",
                                          "Exmaple of C893312.")
trn_validator = validators.RegexValidator(r"^[^0$]",
                                          "You should have 10 characters.")


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


# class EmployeeCreateForm(forms.ModelForm):
#     title = forms.Select()
#     first_name = forms.CharField(label="First Name",
#                                  widget=forms.TextInput(),
#                                  required=True)
#     last_name = forms.CharField(label="Last Name",
#                                 widget=forms.TextInput(),
#                                 required=True)
#     employee_number = forms.CharField(
#         label="Employee #",
#         required=True,
#         widget=forms.TextInput(attrs={'type': 'number'}))
#     nis = forms.CharField(label="National Insurance #",
#                           required=True,
#                           validators=[nis_validator],
#                           widget=forms.TextInput())
#     trn = forms.CharField(label="Tax Registration #",
#                           required=True,
#                           validators=[trn_validator],
#                           widget=forms.TextInput(attrs={'type': 'number'}))

#     job_title = forms.Select()
#     department = forms.Select()
#     payment = forms.Select(attrs={'onchange': 'check_for_bank()'})
#     bank = forms.Select()
#     bank_account = forms.CharField(
#         required=False, widget=forms.TextInput(attrs={'type': 'text'}))
#     payment_schedule = forms.Select()
#     basic_pay = forms.CharField(required=False,
#                                 label="Base Pay",
#                                 widget=forms.TextInput(attrs={
#                                     'type': 'number',
#                                     'min': 0,
#                                     'step': 0.01
#                                 }))
#     employment_date = forms.DateField(required=False, widget=DatePicker())
#     departure_date = forms.DateField(required=False, widget=DatePicker())
#     is_active = forms.BooleanField(required=False, label='Active?')
#     rate = forms.FloatField(required=False,
#                             widget=forms.TextInput(attrs={
#                                 'type': 'number',
#                                 'min': 0,
#                                 'step': 0.01
#                             }))

#     class Meta:
#         model = Employee
#         fields = (
#             'title',
#             'first_name',
#             'last_name',
#             'trn',
#             'nis',
#             'employee_number',
#             'job_title',
#             'department',
#             'payment',
#             'bank',
#             'bank_account',
#             'payment_schedule',
#             'basic_pay',
#             'employment_date',
#             'departure_date',
#             'is_active',
#             'rate',
#         )


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
                          validators=[nis_validator],
                          widget=forms.TextInput())
    trn = forms.IntegerField(label="Tax Registration #",
                             required=True,
                             validators=[trn_validator],
                             widget=forms.TextInput(
                                 attrs={
                                     'type': 'number',
                                     'min_length': 9,
                                     'max_length': 9,
                                     'min': 0,
                                     'step': 1
                                 }))

    job_title = forms.Select()
    department = forms.Select()
    payment = forms.Select(attrs={'onchange': 'check_for_bank()'})
    bank = forms.Select()
    bank_account = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'type': 'text'}))
    payment_schedule = forms.Select()
    basic_pay = forms.CharField(required=False,
                                label="Base Pay",
                                initial=0,
                                widget=forms.TextInput(attrs={
                                    'type': 'number',
                                    'min': 0,
                                    'step': 0.01
                                }))
    employment_date = forms.DateField(
        required=False, widget=DatePicker(attrs={'autocomplete': 'false'}))
    # departure_date = forms.DateField(required=False, widget=DatePicker())
    is_active = forms.BooleanField(required=False, label='Active?')
    rate = forms.FloatField(initial=0,
                            required=False,
                            widget=forms.TextInput(attrs={
                                'type': 'number',
                                'min': 0,
                                'step': 0.01
                            }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Submit', css_class='btn btn-outline-info'))
        # self.helper.add_input(
        #     Submit('reset', 'Cancel', css_class='btn btn-outline-secondary'))
        self.helper.layout = Layout(
            Row(Column('title', css_class='form-group col-md-2 mb-0'),
                Column('first_name', css_class='form-group col-md-5 mb-0'),
                Column('last_name', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'),
            Row(),
            Row(Column('employee_number',
                       css_class='form-group col-md-4 mb-0'),
                Column('nis', css_class='form-group col-md-4 mb-0'),
                Column('trn', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'),
            Row(Column('department', css_class='form-group col-md-6 mb-0'),
                Column('job_title', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            Row(Column('payment', css_class='form-group col-md-4 mb-0'),
                Column('bank', css_class='form-group col-md-4 mb-0'),
                Column('bank_account', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'),
            Row(Column('rate', css_class='form-group col-md-4 mb-0'),
                Column('payment_schedule',
                       css_class='form-group col-md-4 mb-0'),
                Column('basic_pay', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'),
            Row(
                Column('employment_date',
                       css_class='form-group col-md-6 mb-0'),
                Column('is_active', css_class='form-group col-md-6 mt-5'),
                # Column('departure_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'))

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


class EmployeeUpdateForm(EmployeeCreateForm):
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


class DeductionCreateForm(forms.ModelForm):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={
            'placeholder': "Eg. National Housing Trust.",
            'type': 'text'
        }))
    short_code = forms.CharField(label="Short Code:",
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Eg. NHT',
                                     'type': 'text'
                                 }))
    short_description = forms.CharField(
        label="Short Description",
        widget=forms.TextInput(attrs={
            'placeholder': 'Eg. NHT PAYM',
            'type': 'text'
        }))
    is_statutory = forms.BooleanField(label="Is Statutory?", )
    employee_rate = forms.DecimalField(
        label="Employee Rate",
        widget=forms.TextInput(attrs={
            'placeholder': 'Eg. 0.225',
            'type': 'number'
        }))
    employer_rate = forms.DecimalField(
        label="Employer Rate",
        widget=forms.TextInput(attrs={
            'placeholder': 'Eg. 0.03',
            'type': 'number',
            'step': '0.01'
        }))
    employer_rate = forms.CharField(
        label="Employee Rate",
        widget=forms.TextInput(attrs={
            'placeholder': 'Eg. 0.03',
            'type': 'number',
            'step': '0.01'
        }))
    max_for_year = forms.DecimalField(
        label="Max for Year.",
        widget=forms.TextInput(attrs={
            'placeholder': 'Eg. 20000',
            'type': 'number',
            'step': '0.01'
        }))

    # ded_bef_or_after = forms.TypedChoiceField(
    #     label="Tax before or after?",
    #     choices=((1, "Before"), (2, "After")),
    #     coerce=lambda x: bool(int(x)),
    #     widget=forms.RadioSelect,
    #     initial='2',
    #     required=True,
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Submit', css_class='btn btn-outline-info'))
        # self.helper.add_input(
        #     Submit('reset', 'Cancel', css_class='btn btn-outline-secondary'))
        self.helper.layout = Layout(
            Row(Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'),
            Row(Column('short_description',
                       css_class='form-group col-md-6 mb-0'),
                Column('short_code', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            Row(Column('employee_rate', css_class='form-group col-md-4 mb-0'),
                Column('employer_rate', css_class='form-group col-md-4 mb-0'),
                Column('max_for_year', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'),
            Row(
                Column('is_statutory', css_class='form-group col-md-4 mb-0'),
                Column('is_active', css_class='form-group col-md-4 mb-0'),
                # Column('ded_bef_or_after',
                #        css_class='form-group col-md-4 mb-0'),
                css_class='form-row'))

    class Meta:
        model = Deduction
        fields = (
            'name',
            'short_code',
            'short_description',
            'employee_rate',
            'employer_rate',
            'max_for_year',
            'is_statutory',
            'is_active',
        )


class DeductionUpdateForm(DeductionCreateForm):
    class Meta:
        model = Deduction
        fields = (
            'name',
            'short_code',
            'short_description',
            'employee_rate',
            'employer_rate',
            'max_for_year',
            'is_statutory',
            'is_active',
        )


PAY_SCHEDULE = (
    ('', '------'),
    (1, 'Weekly'),
    (2, 'Forthnightly'),
    (3, 'Monthly'),
)


class TimeSheetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-exampleForm'
        # self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

    pay_schedule = forms.ChoiceField(choices=PAY_SCHEDULE)
    hours_worked = forms.DecimalField()
    pay_rate = forms.DecimalField()
    gross_pay = forms.DecimalField(widget=forms.TextInput(
        attrs={'readonly': '(Optional) any allowances'}))
    allowances = forms.DecimalField(widget=forms.TextInput(
        attrs={
            'type': 'number',
            'min': 0,
            'step': 1,
            'placeholder': '(Optional) any allowances'
        }))
    other_deductions = forms.DecimalField(
        label="Other Deductions",
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'min': 0,
                'step': 1,
                'placeholder': '(Optional) any deductions'
            }))

    #self.helper.form_action = 'submit_survey'
    # self.helper.add_input(Submit('submit', 'Save Time Sheet'))
