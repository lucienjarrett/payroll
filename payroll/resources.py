#https://django-import-export.readthedocs.io/en/latest/getting_started.html#exporting-data

from import_export import resources
from .models import Employee


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        exclude = ('allowances' 'title', )
        skip_unchanged = True
        report_skipped = False
        # import_id_fields = ('employee_number', )
        # fields = ('id', 'name', 'author', 'price',)
        # export_order = ('id', 'price', 'author', 'name')
