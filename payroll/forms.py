from django.db.models.fields import CharField, FloatField
from django.core import validators
from django import forms
from django.forms import TextInput, widgets
from django.forms.widgets import DateInput
from .models import (Deduction, Salary, Employee, Allowance, EmployeeAllowance)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

nis_validator = validators.RegexValidator(r"[A-Z]{1}\d{6}$",
                                          "Exmaple of C893312.")
trn_validator = validators.RegexValidator(r"^[^0$]",
                                          "You should have 10 characters.")
# class MyForm(forms.Form):

#     subject = forms.CharField(
#         label="Test field",
#         required=True,  # Note: validators are not run against empty fields
#         validators=[my_validator])


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
                          validators=[nis_validator],
                          widget=forms.TextInput())
    trn = forms.CharField(label="Tax Registration #",
                          required=True,
                          validators=[trn_validator],
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Create', css_class='btn btn-outline-info'))
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
            Row(Column('is_statutory', css_class='form-group col-md-4 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),
                Column('ded_bef_or_after',
                       css_class='form-group col-md-4 mb-0'),
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
            'status',
            'ded_bef_or_after',
        )


class DeductionUpdateForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Update', css_class='btn btn-outline-info'))

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
            Row(Column('is_statutory', css_class='form-group col-md-4 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),
                Column('ded_bef_or_after',
                       css_class='form-group col-md-4 mb-0'),
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
            'status',
            'ded_bef_or_after',
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

PAY_SCHEDULE = (
    ('', '------'),
    (1, 'Weekly'),
    (2, 'Forthnightly'),
    (3, 'Monthly'),
    # (3, 'Yearly'),
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
