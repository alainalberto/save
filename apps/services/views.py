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
      FileFormSet = inlineformset_factory(
          Folder,
          File,
          form=FileForm,
          fields=['name',
                  'url',
                  ],
          extra=5
      )

      def get(self, request, *args, **kwargs):
          form = self.form_class(initial=self.initial)
          form_file = self.FileFormSet()
          return render(request, self.template_name, {'form_company': form, 'form_file': form_file, 'title': 'Create new Company'})

      def post(self, request, *args, **kwargs):
          form = self.form_class(request.POST)
          form_file = self.FileFormSet(request.POST, request.FILES)
          if form.is_valid() and form_file.is_valid():
              company_exist = Companie.objects.filter(name=form.data['name'], ein=form.data['ein'])
              if company_exist:
                  messages.error(request, 'The Company already exists')
                  form = self.form_class(initial=self.initial)
                  return render(request, self.template_name, {'form_company': form, 'form_file': form_file, 'title': 'Create new Company'})
              else:
                  company = form.save(commit=False)
                  customer = Customer.objects.get(id_cut=company.customers_id)
                  folder = Folder.objects.get(id_fld=customer.folders_id)
                  company.folders_id = folder.id_fld
                  company.users_id = request.user.id
                  company.save()
                  files = form_file.save(commit=False)
                  for file in files:
                      file.description = file.name
                      file.date_save = company.created_date
                      file.folders_id = folder.id_fld
                      file.users_id = request.user.id
                      file.save()

                  accion_user(customer, ADDITION, request.user)
                  messages.success(request, 'The customer was saved successfully')
                  return HttpResponseRedirect(reverse_lazy('accounting:customer_view', customer.id_cut))
          else:
              for er in form.errors:
                  messages.error(request, "ERROR: " + er)
              return render(request, self.template_name, {'form_company': form, 'form_file': form_file, 'title': 'Create new Company'})

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
    success_url = reverse_lazy('services:folder')

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.all()
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'customers':customer, 'title': 'Create new Folder'})

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(id_cut=request.POST['customers'])
        user = request.user
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
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'title': 'Create new File'})


class FolderEdit(UpdateView):
    model = File
    form_class = FileForm
    template_name = 'services/folder/folderForm.html'
    success_url = reverse_lazy('services:forms')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_fil = kwargs['pk']
        file = self.model.objects.get(id_fil=id_fil)
        form = self.form_class(request.POST, request.FILES, instance=file)
        if form.is_valid():
            file =form.save()
            accion_user(file, CHANGE, request.user)
            messages.success(request, "File update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit File'})

class FolderDelete(DeleteView):
    model = File
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('services:forms')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_fil = kwargs['pk']
        file = self.model.objects.get(id_fil=id_fil)
        accion_user(file, DELETION, request.user)
        file.delete()
        messages.success(request, "File delete with an extension")
        return HttpResponseRedirect(self.success_url)