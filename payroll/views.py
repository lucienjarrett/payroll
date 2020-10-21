from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from .models import Employee


class EmployeeCreateView(CreateView):
    model = Employee
    fields = ['first_name', 'last_name', 'gender', 'status']

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


# Create your views here.
def about(request):
    return HttpResponse("<h1> About page </h1>")


def contact(request):
    return HttpResponse("</h1> Contacts page </h1>")


def dashboard(request):
    return HttpResponse("<h1> Dashboard page </h1>")


def help(request):
    return HttpResponse("<h1> Help page</h1>")