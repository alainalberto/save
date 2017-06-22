from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.forms import inlineformset_factory
from django.contrib import messages
from FirstCall.util import accion_user
from apps.accounting.components.AccountingForm import *
from apps.accounting.models import *
from apps.logistic.models import Load
from apps.services.components.ServicesForm import *
from apps.services.models import *
from apps.tools.models import Folder


# Create your views here.


class AccountingPanel(View):
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
         messages.success(request,"Account saved with an extension")
         accion_user(account, ADDITION, request.user)
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

def AccountsDescAllViews(request):
    contexto = {}
    accounts = AccountDescrip.objects.all()
    if accounts:
        contexto = {'accounts': accounts}
    return render(request, 'accounting/accounts/accountsDescrp.html', contexto)

def AccountDocument(request, pk):
    accountDescrp = AccountDescrip.objects.get(id_acd=pk)
    if accountDescrp:
        if accountDescrp.type:
            return redirect('/accounting/'+accountDescrp.type+'/edit/'+str(accountDescrp.document)+'/')
    return redirect('accounting:accounts')

# Customers
class CustomersView(ListView):
    model = Customer
    template_name = 'accounting/customer/customerViews.html'

class CustomersCreate(CreateView):
     model = Customer
     form_class = CustomerForm
     template_name = 'accounting/customer/customerForm.html'
     success_url = reverse_lazy('accounting:customers')

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Customer'})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         folders = Folder.objects.filter(name='Customers')
         if not folders:
             Folder.objects.create(name='Customers', description='Customers', folder='NULL')
         folder_father = Folder.objects.get(name='Customers')
         if form.is_valid():
             if not Customer.objects.get(email__contains=form.data['email'], fullname__contains=form.data['fullname']):
                 folder = Folder.objects.create(name=form.data['fullname']+"_Customer", description=form.data['fullname']+"_Customer", folder = folder_father.id_fld)
                 customer = form.save(commit=False)
                 customer.folders_id = folder.id_fld
                 customer.users_id = user.id
                 customer.save()
                 accion_user(customer, ADDITION, request.user)
                 return HttpResponseRedirect(self.success_url)
             else:
                 messages.error(request,"The customer matches")
                 return HttpResponseRedirect(reverse_lazy('accounting:customer_create'))

class CustomersEdit(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'accounting/customer/customerForm.html'
    success_url = reverse_lazy('accounting:customers')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cut = kwargs['pk']
        customer = self.model.objects.get(id_cut=id_cut)
        form = self.form_class(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            accion_user(customer, CHANGE, request.user)
            return HttpResponseRedirect(self.success_url)


class CustomersDelete(DeleteView):
    model = Customer
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customers')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cut = kwargs['pk']
        customer = self.model.objects.get(id_cut=id_cut)
        folder = Folder.objects.get(id_fld=customer.folders_id)
        files = File.objects.filter(folders_id=folder.id_fld)
        folder.delete()
        accion_user(customer, DELETION, request.user)
        customer.delete()
        if files:
          for fl in files:
            file = File.objects.get(id_fil=fl.id_fil)
            file.delete()
        return HttpResponseRedirect(self.success_url)


class CustomersService(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'accounting/customer/customerServices.html'
    form_company_class = CompanyForm
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


#Employees
class EmployeesView(ListView):
    model = Employee
    template_name = 'accounting/employees/employeesViews.html'

class EmployeesCreate(CreateView):
     model = Employee
     form_class = EmployeesForm
     template_name = 'accounting/employees/employeesForm.html'
     success_url = reverse_lazy('accounting:employees')

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Employee'})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         if form.is_valid():
             employee=form.save()
             accion_user(employee, ADDITION, request.user)
             return HttpResponseRedirect(self.success_url)


class EmployeesEdit(UpdateView):
    model = Employee
    form_class = EmployeesForm
    template_name = 'accounting/employees/employeesForm.html'
    success_url = reverse_lazy('accounting:employees')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_ = kwargs['pk']
        employee = self.model.objects.get(id_emp=id)
        form = self.form_class(request.POST, instance=employee)
        if form.is_valid():
            employee =form.save()
            accion_user(employee, CHANGE, request.user)
            return HttpResponseRedirect(self.success_url)

class EmployeesDelete(DeleteView):
    model = Employee
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:employees')


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        employee = self.model.objects.get(id_emp=id)
        accion_user(employee, DELETION, request.user)
        employee.delete()
        return HttpResponseRedirect(self.success_url)

#Invoices
class InvoicesView(ListView):
    model = Invoice
    template_name = 'accounting/invoices/invoicesViews.html'

def InvoicesCreate(request):
    ItemFormSet = inlineformset_factory(
                          Invoice,
                          InvoicesHasItem,
                          form=ItemHasInvoiceForm,
                          fields=['quantity',
                                  'description',
                                  'accounts',
                                  'value',
                                  'tax',
                                  'subtotal'],
                           extra=10
    )
    form = InvoicesForm()
    formset = ItemFormSet()
    items = Item.objects.all()
    loads = Load.objects.all().order_by('number')
    accounts = []
    inc = Account.objects.get(primary=True, name='Income')
    inc_acconts = Account.objects.filter(accounts_id_id=inc.id_acn)
    for i in inc_acconts:
        accounts.append(i)
    for a in inc_acconts:
        exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
        if exp_accont != None:
            for ac in exp_accont:
                accounts.append(ac)
    if request.method == 'POST':
        form = InvoicesForm(request.POST)
        formset = ItemFormSet(request.POST)
        user = request.user
        invs = Invoice.objects.filter(business_id=form.data['business']).order_by('-serial')
        serial = 1
        serials = []
        for s in invs:
            serials.append(s.serial)
        if form.is_valid() and formset.is_valid():
            if serials:
                serial = int(serials[0]) + 1
            invoice = form.save(commit=False)
            invoice.serial = serial
            invoice.users_id = user.id
            if request.POST['btnService']:
                invoice.type = request.POST['btnService']
                invoice.save()
                accion_user(invoice, ADDITION, request.user)
                itemhasInv = formset.save(commit=False)

                for itinv in itemhasInv:
                   if Item.objects.filter(name__contains=itinv.description):
                      item = Item.objects.get(name=itinv.description)
                      itinv.items_id = item.id_ite
                      itinv.invoices = invoice
                      itinv.save()
                      acountDescp = AccountDescrip.objects.create(date=invoice.start_date,
                                                                value=itinv.subtotal,
                                                                accounts_id=itinv.accounts_id,
                                                                document=invoice.id_inv,
                                                                users_id=user.id,
                                                                type='invoices')
                   else:
                       item = Item.objects.create(name=itinv.description, value=itinv.value, accounts_id=itinv.accounts_id )
                       itinv.items_id = item.id_ite
                       itinv.invoices = invoice
                       itinv.save()
                       acountDescp = AccountDescrip.objects.create(date=invoice.start_date,
                                                                   value=itinv.subtotal,
                                                                   accounts_id=itinv.accounts_id,
                                                                   document=invoice.id_inv,
                                                                   users_id=user.id,
                                                                   type='invoices')
            else:
                itemtList = request.data['tbItem'].rows()
            return HttpResponseRedirect(reverse_lazy('accounting:invoices'))
    return render(request, 'accounting/invoices/invoicesForm.html', {
        'form': form,
        'formset': formset,
        'items': items,
        'loads': loads,
        'accounts': accounts,
        'title': 'Create new Invoice'
    })

def InvoicesEdit(request, pk):
    ItemFormSet = inlineformset_factory(
        Invoice,
        InvoicesHasItem,
        form=ItemHasInvoiceForm,
        fields=['quantity',
                'description',
                'accounts',
                'value',
                'tax',
                'subtotal'],
        extra=10
    )
    invoice = Invoice.objects.get(id_inv=pk)
    invitem = InvoicesHasItem.objects.filter(invoices_id=invoice.id_inv)
    items = Item.objects.all()
    loads = Load.objects.all().order_by('number')
    accounts = []
    inv = Account.objects.get(primary=True, name='Income')
    inv_acconts = Account.objects.filter(accounts_id_id=inv.id_acn)
    for e in inv_acconts:
        accounts.append(e)
    for a in inv_acconts:
        exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
        if exp_accont != None:
            for ac in exp_accont:
                accounts.append(ac)
    if request.method == 'GET':
        formset = ItemFormSet()
        form = InvoicesForm(instance=invoice)
    else:
        formset = ItemFormSet(request.POST, instance=invitem)
        form = InvoicesForm(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            form.save()
            if request.POST['btnService']:
                accion_user(invoice, CHANGE, request.user)
                itemhasInv = formset.save(commit=False)

                for itinv in itemhasInv:
                    if Item.objects.filter(name__contains=itinv.description):
                        item = Item.objects.get(name=itinv.description)
                        itinv.items_id = item.id_ite
                        itinv.invoices = invoice
                        itinv.save()
                        acountDescp = AccountDescrip.objects.get(date=invoice.start_date, accounts_id=itinv.accounts_id, document=invoice.id_inv, type='invoices').update(value=itinv.subtotal)

                    else:
                        item = Item.objects.create(name=itinv.description, value=itinv.value,
                                                   accounts_id=itinv.accounts_id)
                        itinv.items_id = item.id_ite
                        itinv.invoices = invoice
                        itinv.save()
                        acountDescp = AccountDescrip.objects.create(date=invoice.start_date,
                                                                    value=itinv.subtotal,
                                                                    accounts_id=itinv.accounts_id,
                                                                    document=invoice.id_inv,
                                                                    users_id=request.user.id,
                                                                    type='invoices')
            return HttpResponseRedirect(reverse_lazy('accounting:invoices'))
    return render(request, 'accounting/invoices/invoicesForm.html', {
        'form': form,
        'formset': formset,
        'items': items,
        'loads': loads,
        'accounts': accounts,
        'title': 'Edit new Invoice'
    })



class InvoicesDelete(DeleteView):
    model = Invoice
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:invoices')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_inv = kwargs['pk']
        invoice = self.model.objects.get(id_inv=id_inv)
        acountDescp = AccountDescrip.objects.get(type='invoices', document=int(invoice.id_inv))
        invitem = InvoicesHasItem.objects.filter(invoices_id=invoice.id_inv)
        acountDescp.delete()
        accion_user(invoice, DELETION, request.user)
        invoice.delete()
        for it in invitem:
            item = InvoicesHasItem.objects.get(id_ind=it.id_ind)
            item.delete()
        return HttpResponseRedirect(self.success_url)

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
         recs = Receipt.objects.filter(business_id=form.data['business']).order_by('-serial')
         serial = 1
         serials = []
         for s in recs:
             serials.append(s.serial)
         if form.is_valid():
             if serials:
               serial = int(serials[0])+1
             receipt = form.save(commit=False)
             receipt.serial = serial
             receipt.users_id = user.id
             receipt.accounts_id = request.POST['account']
             receipt.save()
             accion_user(receipt, ADDITION, request.user)
             acountDescp = AccountDescrip.objects.create(date=form.data['start_date'],
                                                         value=form.data['total'],
                                                         accounts_id=request.POST['account'],
                                                         document=receipt.id_rec,
                                                         users_id=user.id,
                                                         type='receipts'
                                                         )
             return HttpResponseRedirect(reverse_lazy('accounting:receipts'))

class ReceiptsEdit(UpdateView):
    model = Receipt
    form_class = ReceiptsForm
    template_name = 'accounting/receipts/receiptsForm.html'

    def get_context_data(self, **kwargs):
        context = super(ReceiptsEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        receipt = self.model.objects.get(id_rec=pk)
        account = Account.objects.filter(id_acn=receipt.accounts_id)
        accounts = []
        exp = Account.objects.get(primary=True, name='Expenses')
        exp_acconts = Account.objects.filter(accounts_id_id=exp.id_acn)
        for e in exp_acconts:
            accounts.append(e)
        for a in exp_acconts:
            exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
            if exp_accont != None:
                for ac in exp_accont:
                    accounts.append(ac)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['id'] = pk
        context['accounts'] = account
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_rec = kwargs['pk']
        receipt = self.model.objects.get(id_rec=id_rec)
        receipt.accounts_id = request.POST['account']
        acountDescp = AccountDescrip.objects.get(accounts_id=request.POST['account'], document=int(receipt.id_rec))
        form = self.form_class(request.POST, instance=receipt)
        if form.is_valid():
            form.save()
            accion_user(receipt, CHANGE, request.user)
            AccountDescrip.objects.filter(id_acd=acountDescp.id_acd).update(
                date=form.data['start_date'],
                value=form.data['total'],
            )
            return HttpResponseRedirect(reverse_lazy('accounting:receipts'))
        else:
            return HttpResponseRedirect(reverse_lazy('accounting:receipts'))


class ReceiptsDelete(DeleteView):
    model = Receipt
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:receipts')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_rec = kwargs['pk']
        receipt = self.model.objects.get(id_rec=id_rec)
        acountDescp = AccountDescrip.objects.get(accounts_id=receipt.accounts_id, document=int(receipt.id_rec))
        acountDescp.delete()
        accion_user(receipt, DELETION, request.user)
        receipt.delete()

        return HttpResponseRedirect(self.success_url)