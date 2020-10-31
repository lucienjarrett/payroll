from django import template
from django.core.validators import ip_address_validator_map
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (CreateView, ListView, UpdateView, FormView)

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from .models import (Company, Contact, Deduction, Employee, Department,
                     JobTitle, Bank, Earning, PaymentMethod, DutyType,
                     PayPeriod, Salary)
from django.shortcuts import render, get_object_or_404
from .forms import SalaryCreateForm, EmployeeCreateForm
import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.urls import reverse
from .filters import EmployeeFilter
from django.contrib.auth.mixins import LoginRequiredMixin


@permission_required('admin.can_add_log_entry')
def contact_upload(request):
    template = "payroll/contact_upload.html"
    contacts = Contact.objects.all()

    prompt = {
        'order':
        'Order of csv should be first_name, last_name, email, ip_address, message',
        'contacts': contacts
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not a csv file.")
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Contact.objects.update_or_create(first_name=column[0],
                                                      last_name=column[1],
                                                      email=column[2],
                                                      ip_address=column[3],
                                                      message=column[4])
        context = {}
        return render(request, template, context)


@permission_required('admin.can_add_log_entry')
def employee_upload(request):
    template = "payroll/employee_upload.html"
    # data = Employee.objects.all()
    prompt = {
        'order':
        'Order of the csv should be first_name, last_name, employee_number,  nis, trn',
        # 'employees': data
    }

    if request.method == "GET":
        return render(request, template, context=prompt)
    try:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(
                request,
                'This is not a csv file, check the file and try again.')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        # for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            print(
                f'{column[0]} {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}'
            )

            obj, created = Employee.objects.update_or_create(
                first_name=column[0],
                last_name=column[1],
                # employee_number=column[2],
                # nis=column[3],
                # trn=column[4],
                rate=column[5],
                defaults={
                    'employee_number': '12345',
                })

        context = {}
        messages.success(request, "Success")
        return render(request, template, context)
    except Exception as e:
        messages.error(request,
                       message="Unable to upload csv file. " + repr(e))
        return HttpResponseRedirect(reverse("employee-upload"))


@permission_required('admin.can_add_log_entry')
def employee_pay_upload(request):
    template = "payroll/employee_pay_upload.html"
    prompt = {'order': 'Please provide employee_number, hours_worked, rate'}

    if request.method == "GET":
        return render(request, template, prompt)

    try:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith(".csv"):
            messages.error(
                request,
                "This is not a csv file, please check the file and try again.."
            )
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            if Employee.objects.filter(employee_number=column[0]).exists():
                emp_id = Employee.objects.get(employee_number=column[0])

                _, created = Salary.objects.update_or_create(
                    employee=emp_id,
                    employee_id=emp_id.id,
                    hours_worked=column[1],
                    rate=column[2],
                )
        context = {}
        messages.success(request, "Uploaded successfully")
        return render(request, template, context)
    except Exception as e:
        messages.error(request,
                       message="Unable to upload csv file. " + repr(e))
        return HttpResponseRedirect(reverse("employee-pay-upload"))


class SalaryListView(LoginRequiredMixin, ListView):
    model = Salary
    paginate_by = 15


class SalaryCreateView(LoginRequiredMixin, CreateView):
    model = Salary
    form_class = SalaryCreateForm

    def get_initial(self, *args, **kwargs):
        initial = super(SalaryCreateView, self).get_initial(**kwargs)
        initial['title'] = 'Post Salary'
        initial['rate'] = 286.60
        return initial


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        return context


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class EarningCreateView(CreateView):
    model = Earning
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EarningCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        return context


class EarningUpdateView(LoginRequiredMixin, UpdateView):
    model = Earning
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EarningUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class EarningListView(LoginRequiredMixin, ListView):
    model = Earning

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EarningListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Earnings'
        return context


class DeductionCreateView(LoginRequiredMixin, CreateView):
    model = Deduction
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DeductionCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        context['title'] = 'Deductions'
        return context


class DeductionUpdateView(LoginRequiredMixin, UpdateView):
    model = Deduction
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DeductionUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        context['title'] = 'Deductions'
        return context


class DeductionListView(LoginRequiredMixin, ListView):
    model = Deduction

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DeductionListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Deductions'

        return context


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Departments'

        return context


class PayPeriodCreateView(LoginRequiredMixin, CreateView):
    model = PayPeriod
    fields = ['name']


class PayPeriodUpdateView(LoginRequiredMixin, UpdateView):
    model = PayPeriod
    fields = ['name']


class PaymentMethodCreateView(LoginRequiredMixin, CreateView):
    model = PaymentMethod
    fields = ['name']


class PaymentMethodUpdateView(LoginRequiredMixin, UpdateView):
    model = PaymentMethod
    fields = ['name']


class DutyTypeCreateView(LoginRequiredMixin, CreateView):
    model = DutyType
    fields = ['name']


class DutyTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = DutyType
    fields = ['name']


class BankCreateView(LoginRequiredMixin, CreateView):
    model = Bank
    fields = ['name', 'short_code']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BankCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class BankUpdateView(LoginRequiredMixin, UpdateView):
    model = Bank
    fields = ['name', 'short_code']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BankUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class BankListView(LoginRequiredMixin, ListView):
    model = Bank


class JobTitleCreateView(LoginRequiredMixin, CreateView):
    model = JobTitle
    fields = ['name']


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    fields = ['name', 'code', 'state']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DepartmentCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        return context


class JobTitleUpdateView(LoginRequiredMixin, UpdateView):
    model = JobTitle
    fields = ['name']


class DepartmentUpdateView(UpdateView):
    model = Department
    fields = ['name', 'code', 'state']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DepartmentUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    # fields = '__all__'
    # # form_class = EmployeeForm
    exclude = ['departure_date']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        return context


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeCreateForm
    # fields = '__all__'
    exclude = ['employment_date', 'departure_date']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        employee_list = Employee.objects.all()
        context['emp_filter'] = EmployeeFilter(self.request.GET,
                                               queryset=employee_list)
        return context

    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     object_list = Employee.objects.filter(
    #         Q(first_name__icontains=query) | Q(last_name__icontains=query))
    #     return object_list
    def get_queryset(self):
        qs = self.model.objects.all()
        filtered_list = EmployeeFilter(self.request.GET, queryset=qs)
        return filtered_list.qs


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    success_url = '/employee'


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee


# Create your views here.
def about(request):
    return HttpResponse("<h1> About page </h1>")


def contact(request):
    return HttpResponse("</h1> Contacts page </h1>")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'payroll/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        # here's the difference:
        context['employees'] = Employee.objects.all().count()
        context['departments'] = Department.objects.all().count()

        return context


class HelpView(TemplateView):
    template_name = 'payroll/help.html'
