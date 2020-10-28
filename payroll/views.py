from django import template
from django.core.validators import ip_address_validator_map
# from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from .models import Contact, Employee, Department, JobTitle, Bank, Payment, PaymentMethod, DutyType, PayPeriod, Salary
from django.shortcuts import render, get_object_or_404
from .forms import SalaryCreateForm
import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.urls import reverse


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


def employee_upload(request):
    template = "payroll/employee_upload.html"
    # data = Employee.objects.all()
    prompt = {
        'order':
        'Order of the csv should be first_name, last_name, employee_number,  nis, trn',
        # 'employees': data
    }

    if request.method == "GET":

        return render(request, template, prompt)
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
                f'{column[0]} {column[1]} {column[2]} {column[3]} {column[4]}')
            _, created = Employee.objects.update_or_create(
                first_name=column[0],
                last_name=column[1],
                employee_number=column[2],
                nis=column[3],
                trn=column[4])

        context = {}
        messages.success(request, "Success")
        return render(request, template, context)
    except Exception as e:
        messages.error(request,
                       message="Unable to upload csv file. " + repr(e))
        return HttpResponseRedirect(reverse("employee-upload"))


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


class BankListView(ListView):
    model = Bank


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
    # form_class = EmployeeForm
    exclude = ['employment_date', 'departure_date', 'classification']


class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = '__all__'
    exclude = ['employment_date', 'departure_date', 'classification']


class EmployeeListView(ListView):
    model = Employee
    paginate_by = 10


class EmployeeDeleteView(DeleteView):
    model = Employee
    success_url = '/employee'


class EmployeeDetailView(DetailView):
    model = Employee


# Create your views here.
def about(request):
    return HttpResponse("<h1> About page </h1>")


def contact(request):
    return HttpResponse("</h1> Contacts page </h1>")


class DashboardView(TemplateView):
    template_name = 'payroll/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        # here's the difference:
        context['employees'] = Employee.objects.all().count()

        return context


class HelpView(TemplateView):
    template_name = 'payroll/help.html'
