import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'employment_date': ['exact'],
        }
