from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from apps.accounting.models import *
from apps.accounting.components.AccountingForm import *


# Create your views here.


class AccountingPanel(ListView):
    model = Accounts
    template_name = 'accounting/panel_account.html'

class CustomersView(ListView):
    model = Customers
    template_name = 'accounting/customer/customerViews.html'

class CustomersCreate(CreateView):
     model = Customers
     form_class = CustomerForm
     template_name = 'accounting/customer/customerForm.html'
     success_url = reverse_lazy('accounting:customers')
     """def post(self, request, *args, **kwargs):
         if Folders.objects.get(name__contains='Customer'):
             id_father = Folders.objects.filter(name='Customer')
             folder = Folders.objects.crate(name=self.request.POST("name")+"_"+self.request.POST("lastname"),
                                            description="Folder to Customer"+self.request.POST("name")+" "+self.request.POST("lastname"),
                                            folders_id_id=id_father.id_fld)
             customer = Customers.objectes.crate(name=self.request.POST("name"), lastname=self.request.POST("lastname"),
                                                 no_social=self.request.POST("no_social"),
                                                 address=self.request.POST("address"), phone=self.request.POST("phone"),
                                                 email=self.request.POST("email"),
                                                 business_id=self.request.POST("business"), folders_id=folder.id_fld,
                                                 users_id=self.request.POST("users"))
         else:
             id_father = Folders.objects.create(name='Customer', description="Folder to Customer", folders_id_id=None)
             folder = Folders.objects.crate(name=self.request.POST("name") + "_" + self.request.POST("lastname"),
                                            description="Folder to Customer" + self.request.POST("name") + " " + self.request.POST("lastname"),
                                            folders_id_id=id_father.id_fld)
             customer = Customers.objectes.crate(name=self.request.POST("name"), lastname=self.request.POST("lastname"),
                                                 no_social=self.request.POST("no_social"),
                                                 address=self.request.POST("address"), phone=self.request.POST("phone"),
                                                 email=self.request.POST("email"),
                                                 business_id=self.request.POST("business"), folders_id=folder.id_fld,
                                                 users_id=self.request.POST("users"))
     """

class CustomersEdit(UpdateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'accounting/customer/customerForm.html'
    success_url = reverse_lazy('accounting:customers')

class CustomersDelete(DeleteView):
    model = Customers
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customers')


class CustomersService(CreateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'accounting/customer/customerServices.html'
    success_url = reverse_lazy('accounting:customers')

class AccountCreate(CreateView):
    model = Accounts
    form_class = AccountForm
    template_name = 'accounting/accounts/accountsForm.html'
    success_url = reverse_lazy('accounting:accounts')

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Accounts.objects.create(name = self.request.POST["name"], description = self.request.POST["description"], accounts_id_id = self.request.POST["accounts_id"], users_id = user.id, primary = None)

class AccountsDescViews(ListView):
    model = AccountDescrip
    template_name = 'accounting/accounts/accountsDescrp.html'


def AccountsViews(requiret):
    primary = Accounts.objects.filter(primary=1)
    lisexp = Accounts.objects.filter(primary=None)
    contexto = {'accounts': lisexp, 'primary': primary}
    return render(requiret, 'accounting/accounts/accountsViews.html', contexto)

#Employees
class EmployeesView(ListView):
    model = Employees
    template_name = 'accounting/employees/employeesViews.html'

class EmployeesCreate(CreateView):
     model = Employees
     form_class = EmployeesForm
     template_name = 'accounting/employees/employeesForm.html'
     success_url = reverse_lazy('accounting:employees')

class EmployeesEdit(UpdateView):
    model = Employees
    form_class = EmployeesForm
    template_name = 'accounting/employees/employeesForm.html'
    success_url = reverse_lazy('accounting:employees')

class EmployeesDelete(DeleteView):
    model = Employees
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:employees')

#Invoices
class InvoicesView(ListView):
    model = Invoices
    template_name = 'accounting/invoices/invoicesViews.html'

class InvoicesCreate(CreateView):
     model = Invoices
     form_class = InvoicesForm
     template_name = 'accounting/invoices/invoicesForm.html'
     success_url = reverse_lazy('accounting:invoices')

class InvoicesEdit(UpdateView):
    model = Invoices
    form_class = InvoicesForm
    template_name = 'accounting/invoices/invoicesForm.html'
    success_url = reverse_lazy('accounting:invoices')

class InvoicesDelete(DeleteView):
    model = Invoices
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:invoices')

