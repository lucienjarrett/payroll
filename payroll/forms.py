from .custom_layout_object import Formset
from django.db.models.fields import CharField, FloatField
from django.core import validators
from django import forms
from django.forms import TextInput, widgets, modelformset_factory
from django.forms.widgets import DateInput
from .models import (Bank, Company, Deduction, Department, PaymentMethod, Salary, Employee, Allowance,
                     EmployeeAllowance, Contact, TimeSheetDetail,
                     TimesheetHeader)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Fieldset, ButtonHolder, HTML, Field, Div
from crispy_forms.bootstrap import TabHolder, Tab
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.forms.models import inlineformset_factory
import re

nis_validator = validators.RegexValidator(r"[A-Z]{1}\d{6}$",
                                          "Exmaple of C893312.")
trn_validator = validators.RegexValidator(r"^[^0$]",
                                          "You should have 10 characters.")


class CompanyForm(forms.ModelForm):
    
     class Meta:
        model = Company
        fields = ['name', 'national_ins_num', 'tax_reg_num', 'status']

class AllowanceCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Create Allowance', css_class='btn btn-outline-info'))        
    class Meta:
        model = Allowance
        include = "__all__"
        exclude = ('updated', 'created', 'modified_by', 'created_by')
class BankCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Add Bank', css_class='btn btn-outline-info'))

        self.helper.layout = Layout(
            Row(Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'),
            Row(Column('short_code', css_class='form-group col-md-6 mb-0'),
                Column('transit_no', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
        )

    class Meta:
        model = Bank
        fields = '__all__'
        exclude = ('updated', 'created')

class BankUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Update Bank', css_class='btn btn-outline-info'))

        self.helper.layout = Layout(
            Row(Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'),
            Row(Column('short_code', css_class='form-group col-md-6 mb-0'),
                Column('transit_no', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
        )

    class Meta:
        model = Bank
        fields = '__all__'
        exclude = ('updated', 'created')



class SalaryCreateForm(forms.ModelForm):
    # hours_worked = forms.FloatField(widget=forms.TextInput(
    #     attrs={'oninput': 'calculate()'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = FormHelper()
        self.helper.attrs = {'novalidate': ''}
        helper.add_input(Submit('submit', 'Save Salary'))
        helper.add_input(Submit('reset', 'Cancel'))
        helper.form_method = 'post'

    class Meta:

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


class ExampleForm(forms.ModelForm):
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
    employment_date = forms.DateField(required=False, widget=DatePicker())
    departure_date = forms.DateField(required=False, widget=DatePicker())
    date_of_birth = forms.DateField(required=False, widget=DatePicker())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', 'Add Employee', css_class='btn btn-outline-info'))
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Personal Details',
                    Row(Column('first_name',
                               css_class='form-group col-md-4 mb-0'),
                        Column('middle_name',
                               css_class='form-group col-md-4 mb-0'),
                        Column('last_name',
                               css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'),
                    Row(Column('gender', css_class='form-group col-md-4 mb-0'),
                        Column('date_of_birth',
                               css_class='form-group col-md-4 mb-0'),
                        Column('', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'),
                    HTML("<hr>"),
                    Row(Column('employee_number',
                               css_class="form-group col-md-4 mb-0"),
                        Column('nis', css_class="form-group col-md-4 mb-0"),
                        Column('trn', css_class="form-group col-md-4 mb-0"),
                        css_class='form-row'),
                ),
                Tab(
                    'Contact Details',
                    Row(Column('address1',
                               css_class="form-group col-md-12 mb-0"),
                        css_class='form-row'),
                    Row(Column('address2',
                               css_class="form-group col-md-12 mb-0"),
                        css_class='form-row'),
                    Row(Column('city_parish',
                               css_class="form-group col-md-6 mb-0"),
                        Column('country',
                               css_class="form-group col-md-6 mb-0"),
                        css_class='form-row'),
                    HTML('<hr>'),
                    Row(Column('phone', css_class="form-group col-md-3 mb-0"),
                        Column('alternate_phone',
                               css_class="form-group col-md-3 mb-0"),
                        Column('email', css_class="form-group col-md-6 mb-0"),
                        css_class='form-row'),
                ),
                Tab(
                    'Job Details',
                    Row(Column('department',
                               css_class='form-group col-md-6 mb-0'),
                        Column('job_title',
                               css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'),
                    Row(Column('rate', css_class='form-group col-md-4 mb-0'),
                        Column('basic_pay',
                               css_class='form-group col-md-4 mb-0'),
                        Column('payment_schedule',
                               css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'),
                    Row(Column('employment_date',
                               css_class='form-group col-md-6 mb-0'),
                        Column('departure_date',
                               css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'),
                ),
                Tab(
                    'Payment Details',
                    Row(Column('payment',
                               css_class='form-group col-md-4 mb-0'),
                        Column('bank', css_class='form-group col-md-8 mb-0'),
                        css_class='form-row'),
                    Row(Column('bank_account',
                               css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'),
                ),
            ), )

    class Meta:
        model = Employee
        fields = ('title', 'first_name', 'last_name', 'trn', 'nis',
                  'employee_number', 'job_title', 'department', 'payment',
                  'bank', 'bank_account', 'payment_schedule', 'basic_pay',
                  'employment_date', 'departure_date', 'is_active', 'rate',
                  'address1', 'address2', 'city_parish', 'country', 'phone',
                  'alternate_phone', 'gender', 'email', 'middle_name',
                  'date_of_birth', 'created_by')


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
    nis = forms.CharField(
        label="National Insurance #",
        required=True,
        #   validators=[nis_validator],
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
            'created_by',
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
    # is_statutory = forms.BooleanField(label="Is Statutory?" )
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
            Submit('submit',
                   'Create Deduction',
                   css_class='btn btn-outline-info'))
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


class PaymentCreateForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit',
                    'Create Payment Method',
                    css_class='btn btn-outline-info'))
        # self.helper.add_input(
        #     Submit('reset', 'Cancel', css_class='btn btn-outline-secondary'))
        self.helper.layout = Layout(
            Row(Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'))
    class Meta:
        model = PaymentMethod
        fields = ('name',)


class PaymentUpdateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit',
                    'Update Payment Method',
                    css_class='btn btn-outline-info'))
        # self.helper.add_input(
        #     Submit('reset', 'Cancel', css_class='btn btn-outline-secondary'))
        self.helper.layout = Layout(
            Row(Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'))
    class Meta:
        model = PaymentMethod
        fields = ('name',)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('ip_address', 'message')
        include = ('first_name', 'last_name', 'email')


ContactFormSet = modelformset_factory(Contact, extra=1, form=ContactForm)



class TimeSheetForm(forms.ModelForm):
    class Meta:
        model = TimeSheetDetail
        exclude = ('modified_by',)


TimeSheetFormSet = inlineformset_factory(TimesheetHeader, TimeSheetDetail, form=TimeSheetForm, extra=1)


class TimesheetDetailForm(forms.ModelForm):
    class Meta:
        
        model = TimesheetHeader
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(TimesheetDetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.help_text_as_placeholder = True
        self.helper.form_show_labels = False
        #remove label from fields
        # for field in TimesheetDetailForm.Meta.unlabelled_fields:
        #     self.fields[field].label = False

        
        
        self.helper.layout = Layout(
            Div(
                Column('location'),
                Column('work_date'),
                Fieldset('Timesheet Details',
                    Formset('times')),
                HTML("<br>"),
                
                ButtonHolder(Submit('submit', 'Save Timesheet', css_class='btn btn-outline-info')),
                )
            )
        
TimesheetDetailFormset = inlineformset_factory(
    parent_model = TimesheetHeader, model=TimeSheetDetail, form=TimesheetDetailForm, 
    fields=['employee', 'date_time_in', 'date_time_out'], extra=0, can_delete=True, 
    min_num=1, validate_min=True)




# class TimesheetDetailForm(forms.ModelForm):
#     class Meta:  
#         model = TimeSheetDetail
#         fields ='__all__'
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         formtag_prefix = re.sub('-[0-9]+$', '', str(kwargs.get('prefix', '')))
#         self.helper = FormHelper()
#         self.helper.form_tag = False
#         # self.helper.form_show_labels = False
#         self.helper.layout = Layout(
#             Row(
#                 Field('employee'),
#                 Field('date_time_in'),
#                 Field('date_time_out'),
#                 Field('hours'),
#                 # Field('DELETE'),
#                 css_class='formset_row-{}'.format(formtag_prefix)
#             )
#         )

        
# TimesheetDetailFormset = inlineformset_factory(
#     parent_model = TimesheetHeader, model=TimeSheetDetail, form=TimesheetDetailForm, 
#     fields=['employee', 'date_time_in', 'date_time_out'], extra=0, can_delete=True, 
#     min_num=1, validate_min=True)


# class TimesheetHeaderForm(forms.ModelForm):
#     class Meta:
#         model = TimesheetHeader
#         fields = ['location', 'comment']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = True
#         self.helper.form_class = 'form-horizontal'
#         # self.helper.label_class = 'col-md-3 create-label'
#         self.helper.field_class = 'col-md-9'
#         self.helper.layout = Layout(
#             Div(
#                 Field('location'),
#                 Field('comment'),
#                 Fieldset('Add times',
#                          Formset('times')),
               
#                 HTML("<br>"),
#                 ButtonHolder(Submit('submit', 'Save')),
#             )
#         )



