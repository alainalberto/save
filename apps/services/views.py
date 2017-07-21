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
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from apps.services.models import *
from apps.tools.models import Folder, Busines, File
from datetime import datetime, date, time, timedelta
from django.contrib import messages
from FirstCall.util import accion_user
from django.template import Template, RequestContext


# Create your views here.
def CompanyView(request, pk):
    company = Companie.objects.get(id_com=pk)
    return render(request, 'services/company/companyView.html', {'company': company})


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
          id = kwargs['pk']
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
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
                    customer = Customer.objects.get(id_cut=id())
                  else:
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
        customer = Customer.objects.filter(deactivated=False)
        if 'form_company' not in context:
            context['form_company'] = self.form_class(instance=company)
        context['id'] = pk
        context['customers'] = customer
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
        id_fil = kwargs['pk']
        file = self.model.objects.get(id_fil=id_fil)
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
        return render(request, self.template_name, {'form_files': form, 'is_popup':popup, 'customers':customer, 'title': 'Create new Folder'})

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

    def get_context_data(self, **kwargs):
        context = super(FolderDelete, self).get_context_data(**kwargs)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        id = self.kwargs.get('pk', 0)
        context['id'] = id
        context['is_popup'] = popup
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_fil = kwargs['pk']
        file = self.model.objects.get(id_fil=id_fil)
        customer = Customer.objects.get(folders=file.folders)
        accion_user(file, DELETION, request.user)
        file.delete()
        messages.success(request, "File delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))