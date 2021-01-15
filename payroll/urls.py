from collections import namedtuple
from django.urls import path
from django.views.generic.edit import BaseDeleteView
from .views import *
from . import views
from django_filters.views import FilterView
from .filters import EmployeeFilter

urlpatterns = [
    path('', DashboardView.as_view(), name="payroll-dashboard"),
    path('payroll/', DashboardView.as_view(), name="payroll-dashboard"),
    path('timesheet', TimeSheetList.as_view(), name="timesheet-list"),      
    path('payroll/timesheet/new', TimeSheetDetailCreateView.as_view(), name="timesheet-create"),
    path('payroll/timesheet/<int:pk>/update', TimeSheetDetailUpdateView.as_view(), name="timesheet-update"),
    path('payroll/timsheet/<int:pk>', TimeSheetDetailView.as_view(), name="timesheet-detail"),
    path('payroll/example/', ExampleView.as_view(), name="example"),
    path('payroll/about/', views.about, name="payroll-about"),
    path('payroll/help/', HelpView.as_view(), name="payroll-help"),
    path('payroll/report/', ReportView.as_view(), name="payroll-report"),
    path('payroll/contact/', views.contact, name="payroll-contact"),
    #Company
    path('company/new', CompanyCreateView.as_view(), name='company-create'),
    path('company/<int:pk>/update',
         CompanyUpdateView.as_view(),
         name='company-update'),
    path('company', CompanyListView.as_view(), name="company-list"),
    path('company/<int:pk>', CompanyDetailView.as_view(), name="company-detail"), 
    path('company/<int:pk>/delete/', CompanyDeleteView.as_view(), name="company-delete"),
    #End Company

    #Start Employee Routes
    path('employee/new/', EmployeeCreateView.as_view(),
         name="employee-create"),
    path('employee/', EmployeeListView.as_view(), name="employee-list"),
    path('employee/<int:pk>/update/',
         EmployeeUpdateView.as_view(),
         name="employee-update"),
    path('employee-delete/<int:pk>/delete/',
         EmployeeDeleteView.as_view(),
         name="employee-delete"),
    path('employee/<int:pk>/',
         EmployeeDetailView.as_view(),
         name="employee-detail"),
    path('employee_upload/', views.employee_upload, name="employee-upload"),
    path('employee_pay_upload/',
         views.employee_pay_upload,
         name="employee-pay-upload"),
    path('employee_simple_upload/',
         views.simple_upload,
         name="employee-simple-upload"),

    #End Employee Routes
    #Salary
    path('salary/', SalaryListView.as_view(), name="salary-list"),
    path('salary/new', SalaryCreateView.as_view(), name="salary-create"),
    path('salary/<int:pk>/update',
         SalaryUpdateView.as_view(),
         name="salary-update"),
    #End Salary
    #Department
    path('department/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('department/new/',
         DepartmentCreateView.as_view(),
         name="department-create"),
    path('department/<int:pk>/update/',
         DepartmentUpdateView.as_view(),
         name="department-update"),
    path('department/', DepartmentListView.as_view(), name='department-list'),
    path('department-delete/<int:pk>/delete/',
         DepartmentDeleteView.as_view(),
         name="department-delete"),
    #End department
    #Jobtitle
    path('jobtitle/new/', JobTitleCreateView.as_view(),
         name="jobtitle-create"),
    path('jobtitle/<int:pk>/update/',
         JobTitleUpdateView.as_view(),
         name="jobtitle-update"),
    path('jobtitle/', JobTitleListView.as_view(), name="jobtitle-list"),
    path('jobtitle/<int:pk>/delete',
         JobTitleDeleteView.as_view(),
         name="jobtitle-delete"),
    path('jobtitle/<int:pk>', JobtitleDetailView.as_view(), name="jobtitle-detail"), 
    #end Jobtitle
    #Start Banks
    path('bank/new/', BankCreateView.as_view(), name="bank-create"),
    path('bank/<int:pk>/update/', BankUpdateView.as_view(),
         name="bank-update"),
    path('bank/', BankListView.as_view(), name="bank-list"),
    path('bank/<int:pk>/delete', BankDeleteView.as_view(), name="bank-delete"),
    path('bank/<int:pk>', BankDetailView.as_view(), name='bank-detail'), 
    #End Banks

    #Start Deductions
    path('deduction/new/',
         DeductionCreateView.as_view(),
         name="deduction-create"),
    path('deduction/<int:pk>/update/',
         DeductionUpdateView.as_view(),
         name="deduction-update"),
    path('deduction/', DeductionListView.as_view(), name="deduction-list"),
    path('deduction/<int:pk>/delete',
         DeductionDeleteView.as_view(),
         name='deduction-delete'),
    path('deduction/<int:pk>',
         DeductionDetailView.as_view(),
         name='deduction-detail'),
    #End Deductions
    path('payment-method/new/',
         PaymentMethodCreateView.as_view(),
         name="paymentmethod-create"),
    path('payment-method/<int:pk>/update/',
         PaymentMethodUpdateView.as_view(),
         name="payment-method-update"),
     path('payment-method/', PaymentMethodListView.as_view(), name="payment-method-list"),
     path('payment-method/<int:pk>/delete/', PaymentMethodDeleteView.as_view(), name="payment-method-delete"), 
     path('payment-method/<int:pk>', PaymentMethodDetailView.as_view(), name="payment-method-detail"), 

    path('duty-type/new/',
         DutyTypeCreateView.as_view(),
         name="dutytype-create"),
    path('duty-type/<int:pk>/update/',
         DutyTypeUpdateView.as_view(),
         name="dutytype-update"),
    path('salary/new/', SalaryCreateView.as_view(), name="salary-create"),

    #Earnings Start
    path('allowance/new/',
         AllowanceCreateView.as_view(),
         name="allowance-create"),
    path('allowance/<int:pk>/update/',
         AllowanceUpdateView.as_view(),
         name="allowance-update"),
    path('allowance/<int:pk>', AllowanceDetailView.as_view(), name="allowance-detail"), 
    path('allowance/', AllowanceListView.as_view(), name="allowance-list"),
    path('allowance/<int:pk>', AllowanceDeleteView.as_view(), name="allowance-delete"),
    #Earnings End
    path('contact_upload/', views.contact_upload, name='upload-contacts'),
    path('contact_formset/',
         views.create_contact_model_form,
         name='contact-model-formset'),
    path('payroll/payslip', PayslipView.as_view(), name='payslip'),
    path('report/new', ReportCreateView.as_view(), name='report-create'),
    #     path('report/<int:pk>/update',
    #          ReportUpdateView.as_view(),
    #          name='report-update'),
]