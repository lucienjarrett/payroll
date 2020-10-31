import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    # first_name = django_filters.CharFilter(lookup_expr='icontains')
    # last_name = django_filters.CharFilter(lookup_expr='icontains')

    # employment_date_joined = django_filters.NumberFilter(
    #     name='employment_date', lookup_expr='year')
    # employment_date__gt = django_filters.NumberFilter(name='employment_date',
    #                                                   lookup_expr='year__gt')
    # employment_date__lt = django_filters.NumberFilter(name='employment_date',
    #                                                   lookup_expr='year__lt')

    # class Meta:
    #     model = Employee
    #     fields = [
    #         'first_name',
    #         'last_name',
    #     ]
    class Meta:
        model = Employee
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'employment_date': ['exact'],
        }
