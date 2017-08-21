from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import inlineformset_factory
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.auth.models import Group, GroupManager
from apps.services.components.ServicesForm import *
from apps.tools.components.AlertForm import AlertForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.services.models import *
from apps.tools.models import Folder, Busines, File, Alert
from datetime import datetime, date, time, timedelta
from django.contrib import messages
from FirstCall.util import accion_user
import os


# Create your views here.
def PermitView(request, pk, popup):
    permit = Permit.objects.get(id_com=pk)
    return render(request, 'services/company/companyView.html', {'permit': permit, 'is_popup':popup, 'title':'Company', 'deactivate':True})


class PermitCreate(CreateView):
      model = Permit
      template_name = 'services/company/companyForm.html'
      form_class = PermitForm

      def get(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          customer = Customer.objects.filter(deactivated=False)
          form = self.form_class(initial=self.initial)
          return render(request, self.template_name, {'form': form, 'customers':customer, 'is_popup': popup, 'title': 'Create Permit'})

      def post(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          form = self.form_class(request.POST)
          if form.is_valid():
              permit_exist = Permit.objects.filter(name=form.data['name'], ein=form.data['ein'])
              if permit_exist:
                  messages.error(request, 'The Company already exists')
                  form = self.form_class(initial=self.initial)
                  return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create Permit'})
              else:
                  permit = form.save(commit=False)
                  if popup:
                    customer = Customer.objects.get(id_cut=id)
                  else:
                      customer = Customer.objects.get(id_cut=request.POST['customers'])
                  permit.customers = customer
                  if not customer.company_name:
                      update_customer = Customer.objects.filter(id_cut=customer.id_cut).update(company_name=permit.name, ein=permit.ein)
                  permit.users_id = request.user.id
                  permit.update = datetime.now().strftime("%Y-%m-%d")
                  if permit.deactivate:
                      permit.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                  else:
                      permit.deactivate_date = None
                  permit.save()
                  if request.POST['txdmv_alert']:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = permit.txdmv_date_exp
                        dateShow = datetime.now() - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires customer TXDMV Permit " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                  if request.POST['ucr_alert']:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        dateExp = permit.ucr_date_exp
                        dateShow = datetime.now() - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires customer UCR Permit " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                  accion_user(permit, ADDITION, request.user)
                  messages.success(request, 'The Permit was saved successfully')
                  return HttpResponseRedirect('/accounting/customers/view/'+str(permit.customers_id))
          else:
              for er in form.errors:
                  messages.error(request, "ERROR: " + er)
              return render(request, self.template_name, {'form': form, 'is_popup': popup,'title': 'Create Permit'})


class PermitEdit(UpdateView):
    model = Permit
    template_name = 'services/company/companyForm.html'
    form_class = PermitForm

    def get_context_data(self, **kwargs):
        context = super(PermitEdit, self).get_context_data(**kwargs)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        company = self.model.objects.get(id_com=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=company)
        context['id'] = pk
        context['is_popup'] = popup
        context['title'] = 'Edit Permit'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
        else:
            popup = 0
        permit = self.model.objects.get(id_com=pk)
        form = self.form_class(request.POST, instance=permit)
        if form.is_valid():
                permit = form.save(commit=False)
                permit.update = datetime.now().strftime("%Y-%m-%d")
                permit.users_id = request.user.id
                if permit.deactivate:
                    permit.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                else:
                    permit.deactivate_date = None
                permit.save()
                if request.POST['txdmv_alert']:
                   dateExp = datetime.strptime(permit.txdmv_date_exp, "%Y-%m-%d")
                   dateShow = datetime.now().strftime("%Y-%m-%d") - timedelta(days=30)
                   alert = Alert.objects.filter(description="Expires customer TXDMV Permit " + str(permit.customers),
                                             end_date=permit.txdmv_date_exp)
                   alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                if request.POST['ucr_alert']:
                   dateExp = datetime.strptime(permit.ucr_date_exp, "%Y-%m-%d")
                   dateShow = datetime.now().strftime("%Y-%m-%d") - timedelta(days=30)
                   alert = Alert.objects.filter(description="Expires customer UCR Permit " + str(permit.customers),
                                             end_date=permit.ucr_date_exp)
                   alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                accion_user(permit, ADDITION, request.user)
                messages.success(request, 'The Permit was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(permit.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name,
                          {'form': form,  'is_popup': popup, 'title': 'Edit Permit'})

class PermitDelete(DeleteView):
    model = Permit
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        permit = self.model.objects.get(id_com=id)
        alert_txdmv = Alert.objects.filter(description="Expires customer TXDMV Permit " + str(permit.customers),
                                     end_date=permit.txdmv_date_exp)
        alert_ucr = Alert.objects.filter(description="Expires customer UCR Permit " + str(permit.customers),
                                           end_date=permit.ucr_date_exp)
        accion_user(permit, DELETION, request.user)
        alert_txdmv.delete()
        alert_ucr.delete()
        permit.delete()
        messages.success(request, "Permit delete with an extension")
        return HttpResponseRedirect(self.success_url)

class FormView(ListView):
    model = File
    template_name = 'services/form/fileViews.html'

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        if Folder.objects.filter(name='Forms'):
            folder_father = Folder.objects.get(name='Forms')
            forms = File.objects.filter(folders=folder_father)
            context['forms'] = forms
            return context

class FormCreate(CreateView):
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


class FormEdit(UpdateView):
    model = File
    form_class = FileForm
    template_name = 'services/form/fileForm.html'
    success_url = reverse_lazy('services:forms')

    def get_context_data(self, **kwargs):
        context = super(FormEdit, self).get_context_data(**kwargs)
        id = self.kwargs.get('pk', 0)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        if 'form' not in context:
            context['form'] = self.form_class
        context['id'] = id
        context['is_popup'] = popup
        context['title'] = 'Edit Form'
        return context

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

class FormDelete(DeleteView):
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
        folder = Folder.objects.all().order_by('name')
        file = File.objects.all().order_by('name')
        paginator = Paginator(folder, 10)  # Show 25 contacts per page

        page = self.request.GET.get('page')
        try:
            folders = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            folders = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            folders = paginator.page(paginator.num_pages)
        context['folders'] = folders
        context['files'] = file
        return context


class FolderCreate(CreateView):
    model = File
    form_class = inlineformset_factory(
        Folder,
        File,
        form=FileForm,
        fields=['name',
                'category',
                'url',
                ],
        extra=10
    )
    template_name = 'services/folder/folderForm.html'


    def get(self, request, *args, **kwargs):
        if kwargs.__contains__('pk'):
            customer = None
        else:
            customer = Customer.objects.filter(deactivated=False)
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form_files': form,  'customers': customer, 'title': 'Create new Folder'})

    def post(self, request, *args, **kwargs):
        user = request.user
        if kwargs.__contains__('pk'):
            id = kwargs['pk']
            customer = Customer.objects.get(id_cut=id)
        else:
            customer = Customer.objects.get(id_cut=request.POST['customers'])
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            folder = Folder.objects.get(id_fld=customer.folders_id)
            file = form.save(commit=False)
            for f in file:
              f.users_id = user.id
              f.folders = folder
              f.save()
            messages.success(request, "Form saved with an extension")
            accion_user(file, ADDITION, request.user)
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form_files': form, 'customers':customer,'title': 'Create new Folder'})


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


def EquipmentView(request, pk, popup):
    permit = Permit.objects.get(id_com=pk)
    return render(request, 'services/company/companyForm.html', {'form': permit, 'is_popup':popup, 'title':'Company', 'deactivate':True})


class EquipmentCreate(CreateView):
      model = Permit
      template_name = 'services/company/companyForm.html'
      form_class = PermitForm

      def get(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          customer = Customer.objects.filter(deactivated=False)
          form = self.form_class(initial=self.initial)
          return render(request, self.template_name, {'form': form, 'customers':customer, 'is_popup': popup, 'title': 'Create Permit'})

      def post(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          form = self.form_class(request.POST)
          if form.is_valid():
              permit_exist = Permit.objects.filter(name=form.data['name'], ein=form.data['ein'])
              if permit_exist:
                  messages.error(request, 'The Company already exists')
                  form = self.form_class(initial=self.initial)
                  return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create Permit'})
              else:
                  permit = form.save(commit=False)
                  if popup:
                    customer = Customer.objects.get(id_cut=id)
                  else:
                      customer = Customer.objects.get(id_cut=request.POST['customers'])
                  permit.customers = customer
                  if not customer.company_name:
                      update_customer = Customer.objects.filter(id_cut=customer.id_cut).update(company_name=permit.name, ein=permit.ein)
                  permit.users_id = request.user.id
                  permit.update = datetime.now().strftime("%Y-%m-%d")
                  if permit.deactivate:
                      permit.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                  else:
                      permit.deactivate_date = None
                  permit.save()
                  if request.POST['txdmv_alert']:
                        groups = Group.objects.filter(name={'System Administrator', 'System Manager', 'Office Specialist'})
                        dateExp = datetime.strptime(permit.txdmv_date_exp, "%Y-%m-%d")
                        dateShow = datetime.now().strftime("%Y-%m-%d") - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            groups = groups,
                            description = "Expires customer TXDMV Permit" + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                  accion_user(permit, ADDITION, request.user)
                  messages.success(request, 'The Permit was saved successfully')
                  return HttpResponseRedirect('/accounting/customers/view/'+str(permit.customers_id))
          else:
              for er in form.errors:
                  messages.error(request, "ERROR: " + er)
              return render(request, self.template_name, {'form': form, 'is_popup': popup,'title': 'Create Permit'})


class EquipmentEdit(UpdateView):
    model = Permit
    template_name = 'services/company/companyForm.html'
    form_class = PermitForm

    def get_context_data(self, **kwargs):
        context = super(PermitEdit, self).get_context_data(**kwargs)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        company = self.model.objects.get(id_com=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=company)
        context['id'] = pk
        context['is_popup'] = popup
        context['title'] = 'Edit Permit'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
        else:
            popup = 0
        permit = self.model.objects.get(id_com=pk)
        form = self.form_class(request.POST, instance=permit)
        if form.is_valid():
                permit = form.save(commit=False)
                permit.update = datetime.now().strftime("%Y-%m-%d")
                permit.users_id = request.user.id
                if permit.deactivate:
                    permit.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                else:
                    permit.deactivate_date = None
                permit.save()
                dateExp = datetime.strptime(permit.txdmv_date_exp, "%Y-%m-%d")
                dateShow = datetime.now().strftime("%Y-%m-%d") - timedelta(days=30)
                alert = Alert.objects.filter(description="Expires customer TXDMV Permit" + str(permit.customers),
                                             end_date=permit.txdmv_date_exp)
                alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                accion_user(permit, ADDITION, request.user)
                messages.success(request, 'The Permit was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(permit.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name,
                          {'form': form,  'is_popup': popup, 'title': 'Edit Permit'})

class EquipmentDelete(DeleteView):
    model = Permit
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        permit = self.model.objects.get(id_com=id)
        alert = Alert.objects.filter(description="Expires customer TXDMV Permit" + str(permit.customers),
                                     end_date=permit.txdmv_date_exp)
        accion_user(permit, DELETION, request.user)
        alert.delete()
        permit.delete()
        messages.success(request, "Permit delete with an extension")
        return HttpResponseRedirect(self.success_url)
