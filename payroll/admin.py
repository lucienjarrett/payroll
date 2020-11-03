from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Employee, Contact
# Register your models here.

admin.site.register(Contact)

# admin.site.register(Employee)


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    pass