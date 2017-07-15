from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.forms import modelform_factory, inlineformset_factory, formset_factory, BaseModelFormSet
from django.contrib import messages
from FirstCall.util import accion_user
from apps.accounting.components.AccountingForm import *
from apps.accounting.models import *
from apps.logistic.models import Load, DispatchHasPayment, DriversHasPayment, LoadsHasFee, InvoicesHasLoad
from apps.services.components.ServicesForm import *
from apps.tools.components.AlertForm import AlertForm
from apps.services.models import *
from apps.tools.models import Folder
from datetime import datetime, date, time, timedelta
import html
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
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)

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
            return redirect('/accounting/'+accountDescrp.type.lower()+'/view/'+str(accountDescrp.document)+'/')
    return redirect('accounting:accounts')

# Customers
class CustomersView(ListView):
    model = Customer
    template_name = 'accounting/customer/customerViews.html'

    def get(self, request, *args, **kwargs):
        customer = self.model.objects.all()
        context ={'title': 'List Customer', 'object_list': customer}
        return render(request, self.template_name, context)

def CustomerView(request, pk):
       customer = Customer.objects.get(id_cut=pk)
       company = Companie.objects.filter(customers=customer)
       permit = Permission.objects.filter(customers=customer)
       files = File.objects.filter(folders=customer.folders)
       note = Note.objects.filter(customers=customer)
       context = {
           'customer': customer,
           'files': files,
           'companys': company,
           'permit': permit,
           'notes': note,
           'title': 'Customer Folder'
       }
       return render(request, 'accounting/customer/customerView.html', context)

class CustomersCreate(CreateView):
     model = Customer
     form_class = CustomerForm
     template_name = 'accounting/customer/customerViews.html'
     success_url = reverse_lazy('accounting:customers')

     def get(self, request, *args, **kwargs):
         if kwargs.__contains__('popup'):
             popup = kwargs['popup']
         else:
             popup = 0
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create new Customer'})

     def post(self, request, *args, **kwargs):
         """user = User.objects.filter(username=request.POST['email'])
            if user_exist:
              user = User.objects.get(username=request.POST['email'])
            else:
                user = User.objects.create_user(username=request.POST['email'],email=request.POST['email'], password=request.POST['phone'],  is_staff=False, is_active=True)"""
         if kwargs.__contains__('popup'):
             popup = kwargs['popup']
         else:
             popup = 0
         form = self.form_class(request.POST)
         folders = Folder.objects.filter(name='Customers')
         if not folders:
             Folder.objects.create(name='Customers', description='Customers', folder='NULL')
         folder_father = Folder.objects.get(name='Customers')
         if form.is_valid():
             customer_exist = Customer.objects.filter(email=form.data['email'], fullname=form.data['fullname'])
             if customer_exist:
                 messages.error(request,'The customer already exists')
                 form = self.form_class(initial=self.initial)
                 return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create new Customer'})
             else:
                 folder = Folder.objects.create(name=form.data['fullname'] + "_Customer",
                                                description=form.data['fullname'] + "_Customer",
                                                folder=folder_father.id_fld)
                 customer = form.save(commit=False)
                 customer.folders_id = folder.id_fld
                 customer.users_id = request.user.id
                 if customer.deactivated:
                     customer.date_deactivated = datetime.now().strftime("%Y-%m-%d")
                 customer.save()
                 accion_user(customer, ADDITION, request.user)
                 messages.success(request,'The customer was saved successfully')
                 return HttpResponseRedirect(self.success_url)
         else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'is_popup': popup,  'title': 'Create new Customer'})


class CustomersEdit(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'accounting/customer/customerViews.html'
    success_url = reverse_lazy('accounting:customers')

    def get_context_data(self, **kwargs):
        context = super(CustomersEdit, self).get_context_data(**kwargs)
        if kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        customer = Customer.objects.get(id_cut=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=customer)
        context['id'] = pk
        context['is_popup'] = popup
        context['title'] = 'Edit Customer'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cut = kwargs['pk']
        customer = self.model.objects.get(id_cut=id_cut)
        form = self.form_class(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            if customer.deactivated:
                customer.date_deactivated = datetime.today().strftime("%Y-%m-%d")
            else:
                customer.date_deactivated = None
            customer.save()
            accion_user(customer, CHANGE, request.user)
            messages.success(request, 'The customer was update successfully')
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Customer'})


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
        messages.success(request, 'The customer was delete successfully')
        return HttpResponseRedirect(self.success_url)


def CustomersService(request):
    FileFormSet = inlineformset_factory(
        Folder,
        File,
        form=FileForm,
        fields=['name',
                'url',
                ],
        extra=10
    )
    IftaFormSet = inlineformset_factory(
        Customer,
        Ifta,
        form=IftaForm,
        fields=['date',
                'state',
                'milles',
                'gallons',
                'trucks',
                ],
        extra=10
    )
    form = CustomerForm()
    form_permit = PermitForm()
    form_company = CompanyForm()
    form_file = FileFormSet()
    form_insurance = InsuranceForm()
    form_ifta = IftaFormSet()
    form_mtt = MTTForm()
    form_title = TitleForm()
    form_plate = PlateForm()
    form_contract = ContractForm()
    form_alert = AlertForm()

    if request.method == 'POST':
        user_exist = User.objects.filter(username=request.POST['email'])
        if user_exist:
            user = User.objects.get(username=request.POST['email'])
        else:
            user = User.objects.create_user(username=request.POST['email'], email=request.POST['email'],
                                            password=request.POST['phone'], is_staff=False, is_active=True)
        formatDate = "%Y/%m/%d"
        date_now = datetime.today()
        user_create = request.user
        form = CustomerForm(request.POST)
        form_company = CompanyForm(request.POST, request.FILES['logo'])
        form_permit = PermitForm(request.POST)
        form_file = FileFormSet(request.POST, request.FILES['url'])
        form_insurance = InsuranceForm(request.POST)
        form_ifta = IftaFormSet(request.POST)
        form_mtt = MTTForm(request.POST)
        form_title = TitleForm(request.POST)
        form_plate = PlateForm(request.POST)
        form_contract = ContractForm(request.POST)
        form_alert = AlertForm(request.POST)
        folders = Folder.objects.filter(name='Customers')
        if not folders:
            Folder.objects.create(name='Customers', description='Customers', folder='NULL')
        folder_father = Folder.objects.get(name='Customers')
        if form.is_valid():
            customer_exist = Customer.objects.filter(email=form.data['email'], fullname=form.data['fullname'])
            if customer_exist:
                messages.error(request, 'The customer already exists')
                form = CustomerForm(initial=request.initial)
                return render(request, 'accounting/customer/customerServices.html', {
                    'form': form,
                    'form_company': form_company,
                    'form_permit': form_permit,
                    'form_ifta': form_ifta,
                    'form_insurance': form_insurance,
                    'form_mtt': form_mtt,
                    'form_contract': form_contract,
                    'form_title': form_title,
                    'form_plate': form_plate,
                    'form_file': form_file,
                    'form_alert': form_alert,
                })
            else:
                folder = Folder.objects.create(name=form.data['fullname'] + "_Customer",
                                               description=form.data['fullname'] + "_Customer",
                                               folder=folder_father.id_fld)
            customer = form.save(commit=False)
            customer.folders_id = folder.id_fld
            customer.users_id = user.id
            customer.save()

            company = form_company.save(commit=False)
            company.customers_id = customer.id_cut
            company.folders_id = folder.id_fld
            company.users_id = user_create.id
            company.created_date = date_now.strftime(formatDate)
            company.save()

            permit = form_permit.save(commit=False)
            permit.date = date_now
            permit.customers_id = customer.id_cut
            permit.users_id = user_create.id
            permit.save()
            if request.POST['txdmv_alert']:
                alert = form_alert.save(commit=False)
                dateExp = datetime.strptime(permit.txdmv_date_exp, formatDate)
                day = int(request.POST['alert_day'])
                dateShow = date_now - timedelta(days=day)
                alert.category = "Urgents"
                alert.description= "Expires customer TXDMV Permit" + customer
                alert.create_date = date_now.strftime(formatDate)
                alert.show_date = dateShow.strftime(formatDate)
                alert.end_date = dateExp.strftime(formatDate)
                alert.users_id = user_create.id
                alert.save()

            insurance = form_insurance.save(commit=False)
            insurance.customers_id = customer.id_cut
            insurance.users_id = user_create.id
            insurance.save()
            if request.POST['policy_alert']:
                alert = form_alert.save(commit=False)
                dateExp = datetime.strptime(insurance.policy_date_exp, formatDate)
                day = int(request.POST['alert_day'])
                dateShow = date_now - timedelta(days=day)
                alert.category = "Urgents"
                alert.description= "Expires customer insurance policy " + customer
                alert.create_date = date_now.strftime(formatDate)
                alert.show_date = dateShow.strftime(formatDate)
                alert.end_date = dateExp.strftime(formatDate)
                alert.users_id = user_create.id
                alert.save()

            contract = form_contract.save(commit=False)
            contract.customer_id = customer.id_cut
            contract.users_id = user_create.id
            contract.save()
            mtt = form_mtt.save(commit=False)
            mtt.contracts_id = contract.id_con
            mtt.customers_id = customer.id_cut
            mtt.users_id = user_create.id
            mtt.save()
            if request.POST['contract_alert']:
                alert = form_alert.save(commit=False)
                dateExp = datetime.strptime(contract.end_date, formatDate)
                day = int(request.POST['alert_day'])
                dateShow = date_now - timedelta(days=day)
                alert.category = "Urgents"
                alert.description= "Expires customer Maintenance Contract " + customer
                alert.create_date = date_now.strftime(formatDate)
                alert.show_date = dateShow.strftime(formatDate)
                alert.end_date = dateExp.strftime(formatDate)
                alert.users_id = user_create.id
                alert.save()

            title = form_title.save(commit=False)
            title.customers_id = customer.id_cut
            title.users_id = user_create.id
            title.save()
            if request.POST['register_alert']:
                alert = form_alert.save(commit=False)
                dateExp = datetime.strptime(title.date_exp_reg, formatDate)
                day = int(request.POST['alert_day'])
                dateShow = date_now - timedelta(days=day)
                alert.category = "Urgents"
                alert.description= "Expires customer Registration(Title) " + customer
                alert.create_date = date_now.strftime(formatDate)
                alert.show_date = dateShow.strftime(formatDate)
                alert.end_date = dateExp.strftime(formatDate)
                alert.users_id = user_create.id
                alert.save()
            if request.POST['inspection_alert']:
                alert = form_alert.save(commit=False)
                dateExp = datetime.strptime(title.date_exp_insp, formatDate)
                day = int(request.POST['alert_day'])
                dateShow = date_now - timedelta(days=day)
                alert.category = "Urgents"
                alert.description= "Expires customer Inspection(Title) " + customer
                alert.create_date = date_now.strftime(formatDate)
                alert.show_date = dateShow.strftime(formatDate)
                alert.end_date = dateExp.strftime(formatDate)
                alert.users_id = user_create.id
                alert.save()


            plate = form_plate.save(commit=False)
            plate.customers_id = customer.id_cut
            plate.users_id = user_create.id
            plate.save()
            if request.POST['plate_alert']:
                alert = form_alert.save(commit=False)
                dateExp = datetime.strptime(plate.date_exp, formatDate)
                day = int(request.POST['alert_day'])
                dateShow = date_now - timedelta(days=day)
                alert.category = "Urgents"
                alert.description= "Expires customer Plate " + customer
                alert.create_date = date_now.strftime(formatDate)
                alert.show_date = dateShow.strftime(formatDate)
                alert.end_date = dateExp.strftime(formatDate)
                alert.users_id = user_create.id
                alert.save()

            ifta = form_ifta.save(commit=False)
            for i in ifta:
                i.customers_id = customer.id_cut
                i.users_id = user_create.id
                i.save()

            files = form_file.save(commit=False)
            for file in files:
                file.description = file.name
                file.date_save = date_now.strftime(formatDate)
                file.folders_id = folder.id_fld
                file.users_id = user_create.id
                file.save()

            accion_user(customer, ADDITION, request.user)
            messages.success(request, "Customer saved with an extension")
    else:
        for er in form.errors:
            messages.error(request, "ERROR: " + er)
        for er in form_company.errors:
            messages.error(request, "ERROR: " + er)

    return render(request, 'accounting/customer/customerServices.html', {
           'form': form,
           'form_company': form_company,
           'form_permit': form_permit,
           'form_ifta': form_ifta,
           'form_insurance': form_insurance,
           'form_mtt': form_mtt,
           'form_contract': form_contract,
           'form_title': form_title,
           'form_plate': form_plate,
           'form_file': form_file,
           'form_alert': form_alert,
})


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
             employee_exist = Employee.objects.filter(email=form.data['email'], social_no=form.data['social_no'])
             if employee_exist:
                 messages.error(request, 'The employee already exists')
                 form = self.form_class(initial=self.initial)
                 return render(request, self.template_name, {'form': form, 'title': 'Create new Employee'})
             else:
               employee=form.save(commit=False)
               if employee.deactivated:
                   employee.date_deactivated = datetime.now().strftime("%Y-%m-%d")
               else:
                   employee.date_deactivated = None
               employee.save()
               accion_user(employee, ADDITION, request.user)
               messages.success(request, 'The employee was saved successfully')
               return HttpResponseRedirect(self.success_url)
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)
             return render(request, self.template_name, {'form': form, 'title': 'Create new Employee'})


class EmployeesEdit(UpdateView):
    model = Employee
    form_class = EmployeesForm
    template_name = 'accounting/employees/employeesForm.html'
    success_url = reverse_lazy('accounting:employees')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_emp = kwargs['pk']
        employee = self.model.objects.get(id_emp=id_emp)
        form = self.form_class(request.POST, instance=employee)
        if form.is_valid():
            employee =form.save(commit=False)
            if employee.deactivated:
                employee.date_deactivated = datetime.now().strftime("%Y-%m-%d")
            else:
                employee.date_deactivated = None
            employee.save()
            accion_user(employee, CHANGE, request.user)
            messages.success(request, "Employee update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit new Employee'})

class EmployeesDelete(DeleteView):
    model = Employee
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:employees')


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_emp = kwargs['pk']
        employee = self.model.objects.get(id_emp=id_emp)
        accion_user(employee, DELETION, request.user)
        employee.delete()
        messages.success(request, "Employee delete with an extension")
        return HttpResponseRedirect(self.success_url)

#Invoices
class InvoicesView(ListView):
    model = Invoice
    template_name = 'accounting/invoices/invoicesViews.html'

def InvoiceView(request, pk):
        invoice = Invoice.objects.get(id_inv=pk)
        invitem = InvoicesHasItem.objects.filter(invoices_id=invoice.id_inv)
        items = Item.objects.all()
        loads = Load.objects.all().order_by('number')
        context = {'invoice': invoice,
                   'invitems': invitem,
                    'id': pk,
                    'items' :items,
                    'loads': loads,
                    'title': 'Invoice',
                   }
        return render(request,'accounting/invoices/invoicesView.html', context)

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
    LoadFormSet = inlineformset_factory(
                          Invoice,
                          InvoicesHasLoad,
                          form=ItemHasInvoiceForm,
                          fields=['id_inl',
                                  'loads'],
                          extra=10
    )
    form = InvoicesForm()
    formset = ItemFormSet()
    formset_load = LoadFormSet()
    items = Item.objects.all()
    loads = Load.objects.all().order_by('number')
    customer = Customer.objects.filter(deactivated=False)
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
                                                                  type='Invoices')
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
                                                                   type='Invoices')
                messages.success(request, "Invoice saved with an extension")
            else:
                invoice.type = request.POST['btnService']
                invoice.save()
                accion_user(invoice, ADDITION, request.user)
                loadhasInv = formset_load.save(commit=False)
                for lodinv in loadhasInv:
                    if Load.objects.filter(id_lod=lodinv.loads_id):
                        load = Load.objects.get(id_lod=lodinv.loads_id)
                        lodinv.invoices = invoice
                        lodinv.save()
                        acountDescp = AccountDescrip.objects.create(date=invoice.start_date,
                                                                    value=invoice.total,
                                                                    accounts_id=request.POST['account'],
                                                                    document=invoice.id_inv,
                                                                    users_id=user.id,
                                                                    type='Invoices')

                messages.success(request, "Invoice saved with an extension")

            return HttpResponseRedirect(reverse_lazy('accounting:invoices'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            for er in formset.errors:
                messages.error(request, "ERROR: " + er)

    return render(request, 'accounting/invoices/invoicesForm.html', {
        'form': form,
        'formset': formset,
        'formset_load': formset_load,
        'items': items,
        'loads': loads,
        'accounts': accounts,
        'customers': customer,
        'title': 'Create new Invoice'
    })

class ItemInlineFormSet(BaseModelFormSet):
    def clean(self):
        super(ItemInlineFormSet, self).clean()

        for form in self.forms:
            name = form.cleaned_data['name'].upper()
            form.cleaned_data['name'] = name
            # update the instance value.
            form.instance.name = name

class InvoicesEdit(UpdateView):
    model = Invoice
    sec_model = InvoicesHasItem
    template_name = 'accounting/invoices/invoicesForm.html'
    form_class = InvoicesForm
    form_class_item = inlineformset_factory(
                          Invoice,
                          InvoicesHasItem,
                          form=ItemHasInvoiceForm,
                          fields=['id_ind',
                                  'quantity',
                                  'description',
                                  'accounts',
                                  'value',
                                  'tax',
                                  'subtotal'],
                          extra=3
    )

    def get_context_data(self, **kwargs):
        context = super(InvoicesEdit, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        invoice = self.model.objects.get(id_inv=pk)
        items = Item.objects.all()
        loads = Load.objects.all().order_by('number')
        customer = Customer.objects.all()
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
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'formset' not in context:
            context['formset'] = self.form_class_item(instance=invoice)
        context['id'] = pk
        context['items'] = items
        context['loads'] = loads
        context['accounts'] = accounts
        context['customers'] = customer
        context['title'] = 'Edit new Invoice'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_inv = kwargs['pk']
        invoice = self.model.objects.get(id_inv=id_inv)
        formset = self.form_class_item(request.POST, instance=invoice)
        form = self.form_class(request.POST, instance=invoice)
        if form.is_valid():
            if request.POST['btnService']:
                form.save()
                accion_user(invoice, CHANGE, request.user)
                itemhasInv = formset.save(commit=False)
                for itinv in itemhasInv:
                    if Item.objects.filter(name__contains=itinv.description):
                        item = Item.objects.get(name=itinv.description)
                        itinv.items_id = item.id_ite
                        itinv.invoices = invoice
                        itinv.save()
                        acountDescp = AccountDescrip.objects.get(date=invoice.start_date, accounts_id=itinv.accounts_id, document=invoice.id_inv, type='Invoices').update(value=itinv.subtotal)
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
                                                                    type='Invoices')
            messages.success(request, "Invoice update with an extension")
            return HttpResponseRedirect(reverse_lazy('accounting:invoices'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            for er in formset.errors:
                messages.error(request, "ERROR: " + er)

class InvoicesDelete(DeleteView):
    model = Invoice
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:invoices')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_inv = kwargs['pk']
        invoice = self.model.objects.get(id_inv=id_inv)
        acountDescp = AccountDescrip.objects.get(type='Invoices', document=int(invoice.id_inv))
        invitem = InvoicesHasItem.objects.filter(invoices_id=invoice.id_inv)
        acountDescp.delete()
        accion_user(invoice, DELETION, request.user)
        invoice.delete()
        for it in invitem:
            item = InvoicesHasItem.objects.get(id_ind=it.id_ind)
            item.delete()
        messages.success(request, "Invoice delete with an extension")
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
                                                         type='Receipts'
                                                         )
             messages.success(request, "Receipt save with an extension")
             return HttpResponseRedirect(reverse_lazy('accounting:receipts'))
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)

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
            messages.success(request, "Receipt update with an extension")
            return HttpResponseRedirect(reverse_lazy('accounting:receipts'))
        else:
            for er in form.errors:
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
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'accounts': accounts, 'form': form, 'title': 'Create new Receipt'})



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
        messages.success(request, "Receipt delete with an extension")
        return HttpResponseRedirect(self.success_url)

#Payment
class PaymentView(ListView):
    model = Payment
    template_name = 'accounting/payments/paymentsViews.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        payment = []
        pay = Payment.objects.all()
        for p in pay:
            payEmp = EmployeeHasPayment.objects.filter(payments_id=p.id_sal)
            payDri = DriversHasPayment.objects.filter(payments_id=p.id_sal)
            payDisp = DispatchHasPayment.objects.filter(payments_id=p.id_sal)
            if payEmp:
                for e in payEmp:
                    payment.append(p, e)
            if payDri:
                for dr in payDri:
                    payment.append(p, dr)
            if payDisp:
                for ds in payEmp:
                    payment.append(p, ds)
        context['payment'] = payment
        return  context



class PaymentCreate(CreateView):
     model = Payment
     form_class = PaymentForm
     template_name = 'accounting/payments/paymentsForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Payment'})

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
                                                         type='Receipts'
                                                         )
             messages.success(request, "Receipt save with an extension")
             return HttpResponseRedirect(reverse_lazy('accounting:receipts'))
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)

class PaymentEdit(UpdateView):
    model = Receipt
    form_class = ReceiptsForm
    template_name = 'accounting/receipts/receiptsForm.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentEdit, self).get_context_data(**kwargs)
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
            messages.success(request, "Receipt update with an extension")
            return HttpResponseRedirect(reverse_lazy('accounting:receipts'))
        else:
            for er in form.errors:
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
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'accounts': accounts, 'form': form, 'title': 'Create new Receipt'})



class PaymentDelete(DeleteView):
    model = Receipt
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:payment')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_rec = kwargs['pk']
        receipt = self.model.objects.get(id_rec=id_rec)
        acountDescp = AccountDescrip.objects.get(accounts_id=receipt.accounts_id, document=int(receipt.id_rec))
        acountDescp.delete()
        accion_user(receipt, DELETION, request.user)
        receipt.delete()
        messages.success(request, "Receipt delete with an extension")
        return HttpResponseRedirect(self.success_url)

class NoteCreate(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'accounting/customer/noteForm.html'

    def get(self, request, *args, **kwargs):
        is_popup = kwargs['popup']
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'is_popup': is_popup, 'title': 'Create new Note'})

    def post(self, request, *args, **kwargs):
        user = request.user
        id = kwargs['pk']
        is_popup = kwargs['popup']
        customer = Customer.objects.get(id_cut=id)
        form = self.form_class(request.POST)
        if form.is_valid():
             note = form.save(commit=False)
             note.customers = customer
             note.users = user
             note.save()
             accion_user(note, ADDITION, request.user)
             return messages.success(request, 'Added your note to customer')
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'is_popup': is_popup, 'title': 'Create new Note'})

class NoteEdit(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'accounting/customer/noteForm.html'

    def get(self, request, *args, **kwargs):
        is_popup = kwargs['popup']
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'is_popup': is_popup, 'title': 'Create new Note'})

    def post(self, request, *args, **kwargs):
        user = request.user
        id = kwargs['pk']
        is_popup = kwargs['popup']
        customer = Customer.objects.get(id_cut=id)
        form = self.form_class(request.POST)
        if form.is_valid():
             note = form.save(commit=False)
             note.customers = customer
             note.users = user
             note.save()
             accion_user(note, ADDITION, request.user)
             return messages.success(request, 'Added your note to customer')
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'is_popup': is_popup, 'title': 'Create new Note'})

class NoteDelete(DeleteView):
    model = Note
    template_name = 'confirm_delete.html'


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        note = self.model.objects.get(id_rec=id)
        customer = Customer.objects.get(id_cut=note.customers_id)
        accion_user(note, DELETION, request.user)
        note.delete()
        messages.success(request, "Receipt delete with an extension")
        return HttpResponseRedirect('accounting/customers/view/'+customer.id_cut)