from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import DashboardView, EmployeeListView, EmployeeCreateView, EmployeeUpdateView
# from django.views import DashboardView, EmployeeListView, EmployeeCreateView, EmployeeUpdateView

# class TestUrls(SimpleTestCase):
#     def test_employee_list_url_is_resolved(self):
#         url = reverse('list')
#         print(url)


class TestUrls(SimpleTestCase):
    def test_dashoboard_url_is_resolved(self):
        url = reverse('payroll-dashboard')
        self.assertEquals(resolve(url).func.view_class, DashboardView)

    def test_employee_list_url_is_resolved(self):
        url = reverse('employee-list')
        self.assertEquals(resolve(url).func.view_class, EmployeeListView)

    def test_employee_create_url_is_resolved(self):
        url = reverse('employee-create')
        self.assertEquals(resolve(url).func.view_class, EmployeeCreateView)

    def test_employee_update_url_is_resolved(self):
        url = reverse('employee-update', args=['update/'])
        self.assertEquals(resolve(url).func.view_class, EmployeeUpdateView)
