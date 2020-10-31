from django.urls import path
from .views import (
    AllowanceCreateView, AllowanceListView, AllowanceUpdateView,
    BankCreateView, BankListView, BankUpdateView, CompanyListView,
    CompanyUpdateView, DashboardView, DeductionCreateView, DeductionListView,
    DeductionUpdateView, DepartmentListView, DutyTypeCreateView,
    DutyTypeUpdateView, EmployeeCreateView, EmployeeDeleteView,
    EmployeeDetailView, EmployeeListView, EmployeeUpdateView,
    DepartmentCreateView, DepartmentUpdateView, HelpView, JobTitleCreateView,
    JobTitleUpdateView, PayPeriodCreateView, PayPeriodUpdateView,
    PaymentMethodCreateView, PaymentMethodUpdateView, SalaryCreateView,
    SalaryListView, CompanyCreateView, SalaryUpdateView)
from . import views
# from django_filters.views import FilterView

urlpatterns = [
    path('', DashboardView.as_view(), name="payroll-dashboard"),
    path('payroll/', DashboardView.as_view(), name="payroll-dashboard"),
    path('payroll/about/', views.about, name="payroll-about"),
    path('payroll/help/', HelpView.as_view(), name="payroll-help"),
    path('payroll/contact/', views.contact, name="payroll-contact"),
    #     path(
    #         'employee_benefit/',
    #         EmployeeEarningCreateView.as_view(
    #             template_name="payroll/employee_benefit.html")),
    #Company
    path('company/new', CompanyCreateView.as_view(), name='company-create'),
    path('company/<int:pk>/update',
         CompanyUpdateView.as_view(),
         name='company-update'),
    path('company', CompanyListView.as_view(), name="company-list"),
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

    #End Employee Routes
    #Salary
    path('salary/', SalaryListView.as_view(), name="salary-list"),
    path('salary/new', SalaryCreateView.as_view(), name="salary-create"),
    path('salary/<int:pk>/update',
         SalaryUpdateView.as_view(),
         name="salary-update"),
    #End Salary
    path('department/new/',
         DepartmentCreateView.as_view(),
         name="department-create"),
    path('department/<int:pk>/update/',
         DepartmentUpdateView.as_view(),
         name="department-update"),
    path('department/', DepartmentListView.as_view(), name='department-list'),
    path('jobtitle/new/', JobTitleCreateView.as_view(),
         name="jobtitle-create"),
    path('jobtitle/<int:pk>/update/',
         JobTitleUpdateView.as_view(),
         name="jobtitle-update"),
    #Start Banks
    path('bank/new/', BankCreateView.as_view(), name="bank-create"),
    path('bank/<int:pk>/update/', BankUpdateView.as_view(),
         name="bank-update"),
    path('bank/', BankListView.as_view(), name="bank-list"),
    #End Banks

    #Start Deductions
    path('dedcution/new/',
         DeductionCreateView.as_view(),
         name="deduction-create"),
    path('deduction/<int:pk>/update/',
         DeductionUpdateView.as_view(),
         name="deduction-update"),
    path('deduction/', DeductionListView.as_view(), name="deduction-list"),
    #End Deductions
    path('payment-method/new/',
         PaymentMethodCreateView.as_view(),
         name="paymentmethod-create"),
    path('payment-method/<int:pk>/update/',
         PaymentMethodUpdateView.as_view(),
         name="dutytype-update"),
    path('duty-type/new/',
         DutyTypeCreateView.as_view(),
         name="dutytype-create"),
    path('duty-type/<int:pk>/update/',
         DutyTypeUpdateView.as_view(),
         name="dutytype-update"),
    path('pay-period/new/',
         PayPeriodCreateView.as_view(),
         name="payperiod-create"),
    path('pay-period/<int:pk>/update/',
         PayPeriodUpdateView.as_view(),
         name="payperiod-update"),
    path('pay-period/new/',
         PayPeriodCreateView.as_view(),
         name="payperiod-create"),
    path('salary/new/', SalaryCreateView.as_view(), name="salary-create"),

    #Earnings Start
    path('allowance/new/',
         AllowanceCreateView.as_view(),
         name="allowance-create"),
    path('allowance/<int:pk>/update/',
         AllowanceUpdateView.as_view(),
         name="allowance-update"),
    path('allowance/', AllowanceListView.as_view(), name="allowance-list"),
    #Earnings End
    path('contact_upload/', views.contact_upload, name='upload-contacts'),
]