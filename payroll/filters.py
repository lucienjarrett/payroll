from django import forms
import django_filters
from .models import Employee

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass
class EmployeeFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr ='icontains', 
                widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'First name'}))
    last_name = django_filters.CharFilter(lookup_expr ='icontains', 
                widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Last name'}))
    employee_number = django_filters.CharFilter(lookup_expr ='icontains', 
                widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Employee #'}))
    # # department = django_filters.Select()
    # departments = NumberInFilter(field_name='department', lookup_expr='in')
    # uncategorized = django_filters.BooleanFilter(field_name='department', lookup_expr='isnull')
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'employee_number')
        # fields = {
        #     'first_name': ['icontains'],
        #     'last_name': ['icontains'],
        #     'employment_date': ['exact', 'year__gt', 'year__lt'],
        # }


