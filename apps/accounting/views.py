from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from apps.accounting.models import *
from apps.accounting.components.AccountingForm import *


# Create your views here.


class AccountingPanel(ListView):
    model = Account
    template_name = 'accounting/panel_account.html'

class CustomersView(ListView):
    model = Customer
    template_name = 'accounting/customer/customerViews.html'

class CustomersCreate(CreateView):
     model = Customer
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
    model = Customer
    form_class = CustomerForm
    template_name = 'accounting/customer/customerForm.html'
    success_url = reverse_lazy('accounting:customers')

class CustomersDelete(DeleteView):
    model = Customer
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customers')


class CustomersService(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'accounting/customer/customerServices.html'
    success_url = reverse_lazy('accounting:customers')

class AccountCreate(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounting/accounts/accountsForm.html'
    success_url = reverse_lazy('accounting:accounts')

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Account.objects.create(name = self.request.POST["name"], description = self.request.POST["description"], accounts_id_id = self.request.POST["accounts_id"], users_id = user.id, primary = False)

class AccountsDescViews(ListView):
    model = AccountDescrip
    template_name = 'accounting/accounts/accountsDescrp.html'


def AccountsViews(requiret):
    primary = Account.objects.filter(primary=True)
    lisexp = Account.objects.filter(primary=False)
    contexto = {'accounts': lisexp, 'primary': primary}
    return render(requiret, 'accounting/accounts/accountsViews.html', contexto)

#Employees
class EmployeesView(ListView):
    model = Employee
    template_name = 'accounting/employees/employeesViews.html'

class EmployeesCreate(CreateView):
     model = Employee
     form_class = EmployeesForm
     template_name = 'accounting/employees/employeesForm.html'
     success_url = reverse_lazy('accounting:employees')

class EmployeesEdit(UpdateView):
    model = Employee
    form_class = EmployeesForm
    template_name = 'accounting/employees/employeesForm.html'
    success_url = reverse_lazy('accounting:employees')

class EmployeesDelete(DeleteView):
    model = Employee
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:employees')

#Invoices
class InvoicesView(ListView):
    model = Invoice
    template_name = 'accounting/invoices/invoicesViews.html'

class InvoicesCreate(CreateView):
     model = Invoice
     form_class = InvoicesForm
     template_name = 'accounting/invoices/invoicesForm.html'
     success_url = reverse_lazy('accounting:invoices')

class InvoicesEdit(UpdateView):
    model = Invoice
    form_class = InvoicesForm
    template_name = 'accounting/invoices/invoicesForm.html'
    success_url = reverse_lazy('accounting:invoices')

class InvoicesDelete(DeleteView):
    model = Invoice
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:invoices')

