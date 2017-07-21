from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.forms import modelform_factory, inlineformset_factory, formset_factory, BaseModelFormSet
from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from apps.logistic.models import Load
from django.contrib import messages
from FirstCall.util import accion_user
from apps.services.components.ServicesForm import *
from apps.tools.components.AlertForm import AlertForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from apps.services.models import *
from apps.tools.models import Folder, Busines, File, Alert
from datetime import datetime, date, time, timedelta
from django.contrib import messages
from FirstCall.util import accion_user



# Create your views here.
def CompanyView(request, pk, popup):
    company = Companie.objects.get(id_com=pk)
    return render(request, 'services/company/companyViews.html', {'form_company': company, 'is_popup':popup, 'title':'Company', 'deactivate':True})


class CompanyCreate(CreateView):
      model = Companie
      template_name = 'services/company/companyViews.html'
      form_class = CompanyForm

      def get(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
          else:
              popup = 0
          form = self.form_class(initial=self.initial)
          customer = Customer.objects.filter(deactivated=False)
          return render(request, self.template_name, {'form_company': form, 'customers': customer, 'is_popup': popup, 'title': 'Create new Company'})

      def post(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          form = self.form_class(request.POST)
          if form.is_valid():
              company_exist = Companie.objects.filter(name=form.data['name'], ein=form.data['ein'])
              if company_exist:
                  messages.error(request, 'The Company already exists')
                  form = self.form_class(initial=self.initial)
                  return render(request, self.template_name, {'form_company': form, 'is_popup': popup, 'title': 'Create new Company'})
              else:
                  company = form.save(commit=False)
                  if popup:
                    customer = Customer.objects.get(id_cut=id)
                  else:
                      customer = Customer.objects.get(id_cut=company.customers_id)
                  folder = Folder.objects.get(id_fld=customer.folders_id)
                  company.folders_id = folder.id_fld
                  company.users_id = request.user.id
                  if company.deactivate:
                      company.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                  else:
                      company.deactivate_date = None
                  company.save()
                  accion_user(customer, ADDITION, request.user)
                  messages.success(request, 'The customer was saved successfully')
                  return HttpResponseRedirect('/accounting/customers/view/'+str(customer.id_cut))
          else:
              for er in form.errors:
                  messages.error(request, "ERROR: " + er)
              return render(request, self.template_name, {'form_company': form, 'is_popup': popup,'title': 'Create new Company'})


class CompanyEdit(UpdateView):
    model = Companie
    template_name = 'services/company/companyViews.html'
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        context = super(CompanyEdit, self).get_context_data(**kwargs)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        company = self.model.objects.get(id_com=pk)
        if 'form_company' not in context:
            context['form_company'] = self.form_class(instance=company)
        context['id'] = pk
        context['is_popup'] = popup
        context['title'] = 'Edit Company'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        popup = kwargs['popup']
        company = self.model.objects.get(id_com=pk)
        form = self.form_class(request.POST, instance=company)
        if form.is_valid():
            company_exist = Companie.objects.filter(name=form.data['name'], ein=form.data['ein'])
            if company_exist:
                messages.error(request, 'The Company already exists')
                form = self.form_class(initial=self.initial)
                return render(request, self.template_name,
                              {'form_company': form, 'is_popup': popup, 'title': 'Create new Company'})
            else:
                company = form.save(commit=False)
                customer = Customer.objects.get(id_cut=company.customers_id)
                folder = Folder.objects.get(id_fld=customer.folders_id)
                company.folders_id = folder.id_fld
                company.users_id = request.user.id
                if company.deactivated:
                    company.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                else:
                    company.deactivate_date = None
                company.save()
                accion_user(customer, ADDITION, request.user)
                messages.success(request, 'The customer was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/'+customer.id_cut)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name,
                          {'form_company': form,  'is_popup': popup, 'title': 'Create new Company'})

class CompanyDelete(DeleteView):
    model = Companie
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        company = self.model.objects.get(id_com=id)
        accion_user(company, DELETION, request.user)
        company.delete()
        messages.success(request, "Company delete with an extension")
        return HttpResponseRedirect(self.success_url)

class FileView(ListView):
    model = File
    template_name = 'services/form/fileViews.html'

class FileCreate(CreateView):
    model = File
    form_class = FileForm
    template_name = 'services/form/fileForm.html'
    success_url = reverse_lazy('services:forms')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'title': 'Create new Form'})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            folder_exist = Folder.objects.filter(name='Forms')
            if not folder_exist:
                folder = Folder.objects.create(name='Forms', description='All Forms')
            else:
                folder = Folder.objects.get(name='Forms')
            file = form.save(commit=False)
            file.users_id = user.id
            file.folders_id = folder.id_fld
            file.description = file.name
            file.save()
            messages.success(request, "Form saved with an extension")
            accion_user(file, ADDITION, request.user)

            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'title': 'Create new Form'})


class FileEdit(UpdateView):
    model = File
    form_class = FileForm
    template_name = 'services/form/fileForm.html'
    success_url = reverse_lazy('services:forms')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_fil = kwargs['pk']
        file = self.model.objects.get(id_fil=id_fil)
        form = self.form_class(request.POST, request.FILES, instance=file)
        if form.is_valid():
            file =form.save()
            accion_user(file, CHANGE, request.user)
            messages.success(request, "File update")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit File'})

class FileDelete(DeleteView):
    model = File
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('services:forms')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        file = self.model.objects.get(id_fil=id)
        accion_user(file, DELETION, request.user)
        file.delete()
        messages.success(request, "File delete")
        return HttpResponseRedirect(self.success_url)

class FolderView(ListView):
    model = File
    template_name = 'services/folder/folderViews.html'

    def get_context_data(self, **kwargs):
        context = super(FolderView, self).get_context_data(**kwargs)
        if Folder.objects.filter(name='Customers'):
            folder_father = Folder.objects.get(name='Customers')
            folder = Folder.objects.filter(folders_id = folder_father.id_fld)
            file = File.objects.all()
            context['folders'] = folder
            context['files'] = file
            return context


class FolderCreate(CreateView):
    model = File
    form_class = inlineformset_factory(
        Folder,
        File,
        form=FileForm,
        fields=['name',
                'url',
                ],
        extra=10
    )
    template_name = 'services/folder/folderForm.html'


    def get(self, request, *args, **kwargs):
        customer = Customer.objects.filter(deactivated=False)
        if kwargs.__contains__('popup'):
            popup = kwargs.get('popup')
        else:
            popup = 0
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form_files': form, 'is_popup': popup, 'customers': customer, 'title': 'Create new Folder'})

    def post(self, request, *args, **kwargs):
        user = request.user
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
            customer = Customer.objects.get(id_cut=id)
        else:
            popup = 0
            customer = Customer.objects.get(id_cut=request.POST['customers'])
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            folder = Folder.objects.get(id_fld=customer.folders_id)
            file = form.save(commit=False)
            for f in file:
              f.users_id = user.id
              f.folders = folder
              f.description = f.name
              f.save()
            messages.success(request, "Form saved with an extension")
            accion_user(file, ADDITION, request.user)
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form_files': form, 'is_popup':popup, 'customers':customer,'title': 'Create new File'})


class FolderEdit(UpdateView):
    model = File
    template_name = 'services/folder/folderForm.html'
    form_class = FileForm

    def get_context_data(self, **kwargs):
        context = super(FolderEdit, self).get_context_data(**kwargs)
        id = self.kwargs.get('pk', 0)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        if 'form_file' not in context:
            context['form_file'] = self.form_class
        context['id'] = id
        context['is_popup'] = popup
        context['title'] = 'Edit File'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_fil = kwargs['pk']
        file = self.model.objects.get(id_fil=id_fil)
        customer = Customer.objects.get(folders=file.folders)
        form = self.form_class(request.POST, request.FILES, instance=file)
        if form.is_valid():
            file =form.save()
            accion_user(file, CHANGE, request.user)
            messages.success(request, "File update")
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form_file': form, 'title': 'Edit File'})

class FolderDelete(DeleteView):
    model = File
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('services:forms')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        file = self.model.objects.get(id_fil=id)
        accion_user(file, DELETION, request.user)
        file.delete()
        messages.success(request, "File delete with an extension")
        return HttpResponseRedirect(self.success_url)


class MttCreate(CreateView):
    model = Maintenance
    template_name = 'services/mtt/mttForm.html'
    form_class_mtt = MTTForm()
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
        fields=['type',
            'period',
            'nex_period',
            'customers',
                ],
        extra=10
    )
    form_class_permit = PermitForm()
    form_class_company = CompanyForm()
    form_class_insurance = InsuranceForm()
    form_class_title = TitleForm()
    form_class_plate = PlateForm()
    form_class_contract = ContractForm()
    form_class_alert = AlertForm()

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.filter(deactivated=False)
        if kwargs.__contains__('popup'):
            popup = kwargs.get('popup')
        else:
            popup = 0
            form_file = self.FileFormSet()
            form_ifta = self.IftaFormSet()
        return render(request, self.template_name, {'is_popup': popup, 'customers': customer,
                                                    'title': 'Create new Folder',
                                                    'form_company': self.form_class_company,
                                                    'form_permit': self.form_class_permit,
                                                    'form_ifta': form_ifta,
                                                    'form_insurance': self.form_class_insurance,
                                                    'form_mtt': self.form_class_mtt,
                                                    'form_contract': self.form_class_contract,
                                                    'form_title': self.form_class_title,
                                                    'form_plate': self.form_class_plate,
                                                    'form_file': form_file,
                                                    'form_alert': self.form_class_alert,})


    def post(self, request, *args, **kwargs):
        user = request.user
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
            customer = Customer.objects.get(id_cut=id)
        else:
            popup = 0
            customer = Customer.objects.get(id_cut=request.POST['customers'])
        form = self.form_class(request.POST, request.FILES)
        formatDate = "%Y/%m/%d"
        date_now = datetime.today()
        form_company = self.form_class_company(request.POST)
        form_permit = self.form_class_permit(request.POST)
        form_file = self.FileFormSet(request.POST, request.FILES['url'])
        form_insurance = self.form_class_insurance(request.POST)
        form_ifta = self.IftaFormSet(request.POST)
        form_mtt = self.form_class_mtt(request.POST)
        form_title = self.form_class_title(request.POST)
        form_plate = self.form_class_plate(request.POST)
        form_contract = self.form_class_contract(request.POST)
        form_alert = self.form_class_alert(request.POST)
        if form_mtt.is_valid():
            contract = form_contract.save(commit=False)
            contract.users = user
            contract.customer=customer
            contract.save()
            mtt = form_mtt.save(commit=False)
            mtt.contracts_id = contract.id_con
            mtt.users = user
            mtt.save()
            if request.POST['contract_alert']:
                alert = form_alert.save(commit=False)
                dateExp = datetime.strptime(contract.end_date, formatDate)
                day = int(request.POST['alert_day'])
                dateShow = date_now - timedelta(days=day)
                alert.category = "Urgents"
                alert.description = "Expires customer Maintenance Contract " + customer
                alert.create_date = date_now.strftime(formatDate)
                alert.show_date = dateShow.strftime(formatDate)
                alert.end_date = dateExp.strftime(formatDate)
                alert.users = user
                alert.save()

            company = form_company.save(commit=False)
            company.customers_id = customer.id_cut
            company.folders = customer.folders
            company.users = user
            company.created_date = date_now.strftime(formatDate)
            company.save()

            permit = form_permit.save(commit=False)
            permit.date = date_now
            permit.customers = customer
            permit.users = user
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
                alert.users = user
                alert.save()

            insurance = form_insurance.save(commit=False)
            insurance.customers_id = customer.id_cut
            insurance.users = user
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
                alert.users = user
                alert.save()

            title = form_title.save(commit=False)
            title.customers_id = customer.id_cut
            title.users = user
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
                alert.users = user
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
                alert.users = user
                alert.save()


            plate = form_plate.save(commit=False)
            plate.customers_id = customer.id_cut
            plate.users = user
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
                alert.users = user
                alert.save()

            ifta = form_ifta.save(commit=False)
            for i in ifta:
                i.customers_id = customer.id_cut
                i.users = user
                i.save()

            files = form_file.save(commit=False)
            for file in files:
                file.description = file.name
                file.date_save = date_now.strftime(formatDate)
                file.folders = customer.folders
                file.users_id = user
                file.save()

            accion_user(mtt, ADDITION, request.user)
            messages.success(request, "Service saved with an extension")
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
        else:
           for er in form_mtt.errors:
             messages.error(request, "ERROR: " + er)
           for er in form_company.errors:
             messages.error(request, "ERROR: " + er)
           for er in form_insurance.errors:
             messages.error(request, "ERROR: " + er)
           for er in form_permit.errors:
             messages.error(request, "ERROR: " + er)
           for er in form_plate.errors:
             messages.error(request, "ERROR: " + er)
           for er in form_title.errors:
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
