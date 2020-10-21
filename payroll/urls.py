from mypayroll.payroll.views import EmployeeCreateView
from django_project.blog.views import PostCreateView
from django.urls import path
from .views import (EmployeeCreateView)
from . import views

urlpatterns = [
    path('', views.dashboard, name="payroll-dashboard"),
    path('payroll/about/', views.about, name="payroll-about"),
    path('payroll/help/', views.help, name="payroll-help"),
    path('payroll/contact/', views.help, name="payroll-contact"),
    path('employee/new/', EmployeeCreateView.as_view(),
         name="employee-create"),
]