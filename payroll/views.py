from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, FormView
from django.views.generic.edit import DeleteView
from .models import Employee, Department, JobTitle, Bank, Payment, PaymentMethod, DutyType, PayPeriod, Salary
from django.shortcuts import render, get_object_or_404
from .forms import SalaryCreateForm


class SalaryCreateView(CreateView):
    model = Salary
    form_class = SalaryCreateForm

    def get_initial(self, *args, **kwargs):
        initial = super(SalaryCreateView, self).get_initial(**kwargs)
        initial['title'] = 'Post Salary'
        initial['rate'] = 286.60
        return initial


class PaymentCreateView(CreateView):
    model = Payment
    fields = '__all__'


class PaymentUpdateView(UpdateView):
    model = Payment
    fields = '__all__'


class PayPeriodCreateView(CreateView):
    model = PayPeriod
    fields = ['name']


class PayPeriodUpdateView(UpdateView):
    model = PayPeriod
    fields = ['name']


class PaymentMethodCreateView(CreateView):
    model = PaymentMethod
    fields = ['name']


class PaymentMethodUpdateView(UpdateView):
    model = PaymentMethod
    fields = ['name']


class DutyTypeCreateView(CreateView):
    model = DutyType
    fields = ['name']


class DutyTypeUpdateView(UpdateView):
    model = DutyType
    fields = ['name']


class BankCreateView(CreateView):
    model = Bank
    fields = ['name', 'short_code']


class BankUpdateView(UpdateView):
    model = Bank
    fields = ['name', 'short_code']


class JobTitleCreateView(CreateView):
    model = JobTitle
    fields = ['name']


class DepartmentCreateView(CreateView):
    model = Department
    fields = ['name', 'code']


class JobTitleUpdateView(UpdateView):
    model = JobTitle
    fields = ['name']


class DepartmentUpdateView(UpdateView):
    model = Department
    fields = ['name']


class EmployeeCreateView(CreateView):
    model = Employee
    fields = '__all__'


class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = [
        'first_name', 'last_name', 'title', 'nis', 'trn', 'employee_number',
        'department', 'job_title', 'rate', 'bank', 'payment', 'bank_account',
        'payment_schedule'
    ]


class EmployeeListView(ListView):
    model = Employee


class EmployeeDeleteView(DeleteView):
    model = Employee
    success_url = '/employee'

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


# Create your views here.
def about(request):
    return HttpResponse("<h1> About page </h1>")


def contact(request):
    return HttpResponse("</h1> Contacts page </h1>")


def dashboard(request):
    return HttpResponse("<h1> Dashboard page </h1>")


def help(request):
    return HttpResponse("<h1> Help page</h1>")