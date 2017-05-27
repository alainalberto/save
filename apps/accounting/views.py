from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntryManager
from apps.logistic.models import Load
from apps.accounting.components.AccountingForm import *
from apps.services.components.ServicesForm import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from apps.accounting.models import *
from apps.services.models import *
from apps.tools.models import Folder, Busines



# Create your views here.


class AccountingPanel(ListView):
    model = Account
    template_name = 'accounting/panel_account.html'
#Account
class AccountCreate(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounting/accounts/accountsForm.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'title': 'Create new Account'})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
         account = form.save(commit=False)
         account.users_id = user.id
         account.save()
         return HttpResponseRedirect(reverse_lazy('accounting:accounts'))


def AccountsViews(request):
    primary = Account.objects.filter(primary=True)
    lisexp = Account.objects.filter(primary=False)
    contexto = {'accounts': lisexp, 'primary': primary}
    return render(request, 'accounting/accounts/accountsViews.html', contexto)


def AccountsDescViews(request, pk):
    contexto = {}
    accounts = AccountDescrip.objects.filter(accounts_id=pk)
    if accounts:
        contexto = {'accounts': accounts}
    return render(request, 'accounting/accounts/accountsDescrp.html', contexto)

# Customers
class CustomersView(ListView):
    model = Customer
    template_name = 'accounting/customer/customerViews.html'

class CustomersCreate(CreateView):
     model = Customer
     form_class = CustomerForm
     template_name = 'accounting/customer/customerForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Customer'})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         folder_father = Folder.objects.get(name = 'Customers')
         if form.is_valid():
             folder = Folder.objects.create(name=form.data['name']+"_Customer", description=form.data['name']+"_Customer", folder = folder_father.id_fld)
             customer = form.save(commit=False)
             customer.folders_id = folder.id_fld
             customer.users_id = user.id
             customer.save()
             return HttpResponseRedirect(reverse_lazy('accounting:customers'))

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
    form_company_class = CompanyForm
    form_permission_class = PermissionForm
    success_url = reverse_lazy('accounting:customers')

    def get_context_data(self, **kwargs):
        contexto = super(CustomersService, self).get_context_data(**kwargs)
        if 'form' not in contexto:
            contexto['form'] = self.form_class(self.request.GET)
        if 'from_company' not in contexto:
            contexto['form_company']= self.form_company_class(self.request.GET)
        return contexto

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        fotm_company = self.form_company_class(request.POST)
        user = request.user
        if form.is_valid() and fotm_company.is_valid():
            folder = Folder.create(name="Customer_"+form.name+"_"+form.lastname)
            customer = form.save(commit=False)
            customer.users = user
            company = fotm_company.save(commit=False)
            company.customers = customer.save()
            company.folders


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

     def get(self, request, *args, **kwargs):
         items = Item.objects.all()
         loads = Load.objects.all().order_by('number')
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'items': items, 'loads': loads, 'title': 'Create new Invoice'})


class InvoicesEdit(UpdateView):
    model = Invoice
    form_class = InvoicesForm
    template_name = 'accounting/invoices/invoicesForm.html'
    success_url = reverse_lazy('accounting:invoices')

class InvoicesDelete(DeleteView):
    model = Invoice
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:invoices')

#Receipts
class ReceiptsView(ListView):
    model = Receipt
    template_name = 'accounting/receipts/receiptsViews.html'

class ReceiptsCreate(CreateView):
     model = Receipt
     form_class = ReceiptsForm
     template_name = 'accounting/receipts/receiptsForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         accounts = []
         exp = Account.objects.get(primary = True, name= 'Expenses')
         exp_acconts = Account.objects.filter(accounts_id_id = exp.id_acn)
         for e in exp_acconts:
            accounts.append(e)
         for a in exp_acconts:
             exp_accont = Account.objects.filter(accounts_id_id = a.id_acn)
             if exp_accont != None:
                 for ac in exp_accont:
                    accounts.append(ac)
         return render(request, self.template_name, {'accounts': accounts, 'form': form, 'title': 'Create new Receipt'})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         recs = Receipt.objects.filter(business_id=form.data['business'])
         serial = 1
         serials = []
         for s in recs:
             serials.append(s.serial)
         if form.is_valid():
             if serials:
               serial = int(max(serials))+1
             receipt = form.save(commit=False)
             receipt.serial = serial
             receipt.users_id = user.id
             receipt.accounts_id = request.POST['account']
             receipt.save()
             acountDescp = AccountDescrip.objects.create(date=form.data['start_date'],
                                                         value=form.data['total'],
                                                         accounts_id=request.POST['account'],
                                                         document=receipt.id_rec,
                                                         users_id=user.id,
                                                         )
             return HttpResponseRedirect(reverse_lazy('accounting:receipts'))

class ReceiptsEdit(UpdateView):
    model = Receipt
    form_class = ReceiptsForm
    template_name = 'accounting/receipts/receiptsForm.html'
    success_url = reverse_lazy('accounting:receipts')



class ReceiptsDelete(DeleteView):
    model = Receipt
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:receipts')


class ReceiptsPDF(View):
    def get(self, request, *args, **kwargs):
        receipt = Receipt.objects.get(id_rec=7)
        data = {
            'date': '27/5/2017',
            'description': 'Prueba de recibo',
            'total': '50,00',
        }
        pdf = render('accounting/receipts/receiptsPrint.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

