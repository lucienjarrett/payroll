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
                     JobTitle, Bank, Allowance, PaymentMethod, DutyType,
                     Salary)
from django.shortcuts import render, get_object_or_404
from .forms import (SalaryCreateForm, EmployeeCreateForm, SalaryUpdateForm,
                    TimeSheetForm)
import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.urls import reverse
from .filters import EmployeeFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
# from django.utils.text import slugify
# from django_filters.views import FilterView
from .resources import EmployeeResource  #import export csv
from tablib import Dataset

PAGINATE = 10


class TimeSheetView(FormView):
    form_class = TimeSheetForm
    template_name = 'payroll/timesheet.html'


def export_csv(request):
    employee_resource = EmployeeResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    return response


def export_xls(request):
    employee_resource = EmployeeResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.xls,
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="employees.xls"'
    return response


@permission_required('admin.can_add_log_entry')
def simple_upload(request):
    template = 'payroll/simple_upload.html'
    prompt = {
        'order':
        'Order of csv should be first_name, last_name, email, ip_address, message',
    }
    if request.method == "GET":
        return render(request, template, prompt)

    if request.method == 'POST':

        employee_resource = EmployeeResource()
        dataset = Dataset()
        new_employees = request.FILES['myfile']

        imported_data = dataset.load(new_employees.read().decode('UTF-8'),
                                     format='csv')

        result = employee_resource.import_data(
            dataset, dry_run=True)  # Test the data import

        for r in result:
            print(result[r])

        if not result.has_errors():
            employee_resource.import_data(dataset,
                                          dry_run=False)  # Actually import now

    return render(request, template)


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

            _, created = Employee.objects.update_or_create(
                first_name=column[0],
                last_name=column[1],
                employee_number=column[2],
                nis=column[3],
                trn=column[4],
                rate=column[5],
            )

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


# class EmployeeEarningCreateView(CreateView):
#     model = EmployeeEarning
#     form_class = EmployeeBenefitsForm


class SalaryListView(LoginRequiredMixin, ListView):
    model = Salary
    paginate_by = PAGINATE

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SalaryListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        context['form'] = SalaryUpdateForm()
        return context


class SalaryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Salary
    form_class = SalaryCreateForm
    success_message = "Success!"

    def get_initial(self, *args, **kwargs):
        initial = super(SalaryCreateView, self).get_initial(**kwargs)
        initial['title'] = 'Post Salary'
        initial['rate'] = 286.60
        return initial


class SalaryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Salary
    form_class = SalaryUpdateForm
    success_message = "Success!"
    exclude = ['date_posted']

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(SalaryUpdateView, self).get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['button'] = 'Update'
    #     return context


class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Company
    fields = '__all__'
    success_message = "Company added successfully.."

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        return context


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    paginate_by = PAGINATE


class CompanyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Company
    fields = '__all__'
    success_message = "Company updated successfully.."

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class AllowanceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Allowance
    fields = '__all__'
    success_message = "Success"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AllowanceCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        return context


class AllowanceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Allowance
    fields = '__all__'
    success_message = "Success"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AllowanceUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class AllowanceListView(LoginRequiredMixin, ListView):
    model = Allowance
    paginate_by = PAGINATE


class DeductionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Deduction
    fields = '__all__'
    success_message = "Success"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DeductionCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        context['title'] = 'Deductions'
        return context


class DeductionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Deduction
    fields = '__all__'
    success_message = "Success"

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
    paginate_by = PAGINATE

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Departments'
        return context


# class PayPeriodCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = PayPeriod
#     fields = ['name']

# class PayPeriodUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = PayPeriod
#     fields = ['name']


class PaymentMethodCreateView(LoginRequiredMixin, SuccessMessageMixin,
                              CreateView):
    model = PaymentMethod
    fields = ['name']


class PaymentMethodUpdateView(LoginRequiredMixin, SuccessMessageMixin,
                              UpdateView):
    model = PaymentMethod
    fields = ['name']


class DutyTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = DutyType
    fields = ['name']


class DutyTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DutyType
    fields = ['name']


class BankCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Bank
    fields = ['name', 'short_code']
    success_message = "Bank successfully updated."

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BankCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class BankUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Bank
    fields = ['name', 'short_code']
    success_message = "Bank successfully updated."

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BankUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class BankListView(LoginRequiredMixin, ListView):
    model = Bank
    paginate_by = PAGINATE

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BankListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Banks'
        return context


class JobTitleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = JobTitle
    fields = ['name']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(JobTitleCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        return context


class JobTitleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = JobTitle
    fields = ['name']
    success_message = "Job title updated successfully.."

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(JobTitleUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class JobTitleListView(LoginRequiredMixin, ListView):
    model = JobTitle
    paginate_by = PAGINATE

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(JobTitleListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Job Titles'

        return context


class JobTitleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = JobTitle
    success_url = '/jobtitle'
    success_message = "Deleted successfully.."


class DepartmentCreateView(LoginRequiredMixin, SuccessMessageMixin,
                           CreateView):
    model = Department
    fields = ['name', 'code', 'state']
    success_message = "Department added successfully."

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DepartmentCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        return context


class DepartmentDeleteView(LoginRequiredMixin, SuccessMessageMixin,
                           DeleteView):
    model = Department
    success_url = '/department'
    success_message = "Deleted successfully.."


class DepartmentUpdateView(LoginRequiredMixin, SuccessMessageMixin,
                           UpdateView):
    model = Department
    fields = ['name', 'code', 'state']
    success_message = "Department updated successfully.."

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DepartmentUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        return context


class EmployeeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    # fields = '__all__'
    # # form_class = EmployeeForm
    exclude = ['departure_date']
    success_message = "Employee created successfully."

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Create'
        context['title'] = 'Employee'
        return context


class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employee
    form_class = EmployeeCreateForm
    # fields = '__all__'
    exclude = ['employment_date', 'departure_date']
    success_message = "Employee updated successfully."

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['button'] = 'Update'
        context['title'] = 'Employee'
        return context


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    paginate_by = PAGINATE

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(EmployeeListView, self).get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     employee_list = Employee.objects.all()
    #     context['filter'] = EmployeeFilter(self.request.GET,
    #                                        queryset=employee_list)
    #     return context

    # def get_queryset(self):
    #     employee_list = self.Employee.objects.all()
    #     employee_list_filtered = EmployeeFilter(self.request.GET,
    #                                             queryset=employee_list)
    #     return employee_list_filtered


class EmployeeDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Employee
    success_url = '/employee'
    success_message = "Deleted successfully.."


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


class ReportView(TemplateView):
    template_name = 'payroll/reports.html'
