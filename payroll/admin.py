from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import (Employee, Contact, Salary, Bank, Company, Customer,
                     Department, JobTitle, Allowance, Deduction, Parish,
                     LeaveType, PaymentMethod)
# Register your models here.

admin.site.register(Contact)
admin.site.register(Bank)
admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(Department)
admin.site.register(JobTitle)
admin.site.register(Allowance)
admin.site.register(Deduction)
admin.site.register(Parish)
admin.site.register(LeaveType)
admin.site.register(PaymentMethod)


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    pass


@admin.register(Salary)
class SalaryAdmin(ImportExportModelAdmin):
    pass