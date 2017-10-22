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

def pagination(request, objects):

        paginator = Paginator(objects, 10)  # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            objs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            objs = paginator.page(paginator.num_pages)
        return objs

def PermitView(request, pk, popup):
    permit = Permit.objects.get(id_com=pk)
    return render(request, 'services/permit/permitView.html', {'permit': permit, 'is_popup':popup, 'title':'Permit', 'deactivate':True})


class PermitCreate(CreateView):
      model = Permit
      template_name = 'services/permit/permitForm.html'
      form_class = PermitForm

      def get(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          customer = Customer.objects.filter(deactivated=False).order_by('company_name')
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
              permit_exist = Permit.objects.filter(name=request.POST['name'], ein=request.POST['ein'])
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
                  permit.users_id = request.user.id
                  permit.update = datetime.now().strftime("%Y-%m-%d")
                  if permit.deactivate:
                      permit.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                  else:
                      permit.deactivate_date = None
                  permit.save()
                  customer.company_name = permit.name+' '+permit.legal_status
                  customer.ein = permit.ein
                  customer.save()
                  if request.POST.get('txdmv_alert', False) and len(request.POST['txdmv_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = permit.txdmv_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the TXDMV Permit of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                  if request.POST.get('ucr_alert', False) and len(request.POST['ucr_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        dateExp = permit.ucr_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the UCR Permit of the customer " + str(customer),
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
    template_name = 'services/permit/permitForm.html'
    form_class = PermitForm

    def get_context_data(self, **kwargs):
        context = super(PermitEdit, self).get_context_data(**kwargs)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        permit = self.model.objects.get(id_com=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=permit)
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
                customer = Customer.objects.get(id_cut=permit.customers_id)
                customer.company_name = permit.name + ' ' + permit.legal_status
                customer.ein = permit.ein
                customer.save()
                if request.POST.get('txdmv_alert', False) and len(request.POST['txdmv_date_exp']) != 0:
                   dateExp = permit.txdmv_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the TXDMV Permit of the customer " + str(customer), category="Urgents")
                   if alert:
                      alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the TXDMV Permit of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(
                        description="Expires the TXDMV Permit of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        alert.delete()
                if request.POST.get('ucr_alert', False) and len(request.POST['ucr_date_exp']) != 0:
                   dateExp = permit.ucr_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the UCR Permit of the customer " + str(customer), category="Urgents")
                   if alert:
                       alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the UCR Permit of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(description="Expires the UCR Permit of the customer " + str(customer), category="Urgents")
                    if alert:
                        alert.delete()
                accion_user(permit, CHANGE, request.user)
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
        alert_txdmv = Alert.objects.filter(description = "Expires the TXDMV Permit of the customer " + str(permit.customers),
                                     end_date=permit.txdmv_date_exp)
        alert_ucr = Alert.objects.filter(description = "Expires the UCR Permit of the customer" + str(permit.customers),
                                           end_date=permit.ucr_date_exp)
        accion_user(permit, DELETION, request.user)
        if alert_txdmv:
          alert_txdmv.delete()
        if alert_ucr:
          alert_ucr.delete()
        customer = permit.customers
        permit.delete()
        messages.success(request, "Permit delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))

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
        folders = pagination(self.request, Folder.objects.all().order_by('name'))
        file = pagination(self.request,File.objects.all().order_by('name'))
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
            customer = pagination(request, Customer.objects.filter(deactivated=False).order_by('company_name'))
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
    equipment = Equipment.objects.get(id_tru=pk)
    return render(request, 'services/equipment/equipmentView.html', {'equipment': equipment, 'is_popup':popup, 'title':'Equipment', 'deactivate':True})


class EquipmentCreate(CreateView):
    model = Equipment
    template_name = 'services/equipment/equipmentForm.html'
    form_class = EquipmentForm

    def get(self, request, *args, **kwargs):
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
        else:
            popup = 0
            customer = Customer.objects.filter(deactivated=False).order_by('company_name')
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form, 'customers': customer, 'is_popup': popup, 'title': 'Create Equipment'})

    def post(self, request, *args, **kwargs):
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
        else:
            popup = 0
        form = self.form_class(request.POST)
        if form.is_valid():
            equipment_exist = Equipment.objects.filter(type=form.data['type'], serial=form.data['serial'])
            if equipment_exist:
                messages.error(request, 'The Equipment already exists')
                form = self.form_class(initial=self.initial)
                return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create Equipment'})
            else:
                equipment = form.save(commit=False)
                if popup:
                    customer = Customer.objects.get(id_cut=id)
                else:
                    customer = Customer.objects.get(id_cut=request.POST['customers'])
                equipment.customers = customer
                equipment.users = request.user
                equipment.update = datetime.now().strftime("%Y-%m-%d")
                if equipment.deactivate:
                    equipment.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                else:
                    equipment.deactivate_date = None
                equipment.save()
                if request.POST.get('plate_alert', False)  and len(request.POST['plate_date_exp']) != 0:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    dateExp = equipment.plate_date_exp
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Plate Equipment Number "+str(equipment.plate_account_number) +" of the customer "+ str(customer),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                if request.POST.get('reg_alert', False) and len(request.POST['title_date_exp_reg']) != 0:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    dateExp = equipment.title_date_exp_reg
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Title Register Equipment Number "+str(equipment.plate_account_number) +" of the customer "+ str(customer),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                if request.POST.get('insp_alert', False) and len(request.POST['title_date_exp_insp']) != 0:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    dateExp = equipment.title_date_exp_insp
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Inspection Equipment Number "+str(equipment.plate_account_number) +" of the customer "+ str(customer),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
                accion_user(equipment, ADDITION, request.user)
                messages.success(request, 'The Permit was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(equipment.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create Equiptment'})


class EquipmentEdit(UpdateView):
    model = Equipment
    template_name = 'services/equipment/equipmentForm.html'
    form_class = EquipmentForm

    def get_context_data(self, **kwargs):
        context = super(EquipmentEdit, self).get_context_data(**kwargs)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        equipment = self.model.objects.get(id_tru=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=equipment)
        context['id'] = pk
        context['is_popup'] = popup
        context['title'] = 'Edit Equipment'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
        else:
            popup = 0
        equipment = self.model.objects.get(id_tru=pk)
        form = self.form_class(request.POST, instance=equipment)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.update = datetime.now().strftime("%Y-%m-%d")
            equipment.users_id = request.user.id
            if equipment.deactivate:
                equipment.deactivate_date = datetime.now().strftime("%Y-%m-%d")
            else:
                equipment.deactivate_date = None
            equipment.save()
            if request.POST.get('plate_alert', False)  and len(request.POST['plate_date_exp']) != 0:
                dateExp = equipment.plate_date_exp
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Plate Equipment Number " + str(equipment.plate_account_number) + " of the customer " + str(equipment.customers))
                if alert:
                    alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Plate Equipment Number " + str(
                            equipment.plate_account_number) + " of the customer " + str(equipment.customers),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
            else:
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Plate Equipment Number " + str(
                        equipment.plate_account_number) + " of the customer " + str(equipment.customers))
                if alert:
                    alert.delete()
            if request.POST.get('reg_alert', False) and len(request.POST['title_date_exp_reg']) != 0:
                dateExp = equipment.title_date_exp_reg
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Title Register Equipment Number " + str(equipment.plate_account_number) + " of the customer " + str(equipment.customers))
                if alert:
                    alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Title Register Equipment Number " + str(
                            equipment.plate_account_number) + " of the customer " + str(equipment.customers),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
            else:
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Title Register Equipment Number " + str(
                        equipment.plate_account_number) + " of the customer " + str(equipment.customers))
                if alert:
                    alert.delete()
            if request.POST.get('insp_alert', False) and len(request.POST['title_date_exp_insp']) != 0:
                dateExp = equipment.title_date_exp_insp
                dateShow = dateExp - timedelta(days=30)
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Inspection Equipment Number " + str(equipment.plate_account_number) + " of the customer " + str(equipment.customers))
                if alert:
                    alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                else:
                    group_admin = Group.objects.get(name='System Administrator')
                    group_manag = Group.objects.get(name='System Manager')
                    group_offic = Group.objects.get(name='Office Specialist')
                    alert = Alert.objects.create(
                        category="Urgents",
                        description="Expires of the Inspection Equipment Number " + str(
                            equipment.plate_account_number) + " of the customer " + str(equipment.customers),
                        create_date=datetime.now().strftime("%Y-%m-%d"),
                        show_date=dateShow.strftime("%Y-%m-%d"),
                        end_date=dateExp.strftime("%Y-%m-%d"),
                        users=request.user)
                    alert.group.add(group_admin, group_manag, group_offic)
            else:
                alert = Alert.objects.filter(
                    category="Urgents",
                    description="Expires of the Inspection Equipment Number " + str(
                        equipment.plate_account_number) + " of the customer " + str(equipment.customers))
                if alert:
                    alert.delete()
            accion_user(equipment, CHANGE, request.user)
            messages.success(request, 'The Equipment was saved successfully')
            return HttpResponseRedirect('/accounting/customers/view/' + str(equipment.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name,
                          {'form': form, 'is_popup': popup, 'title': 'Edit Equipment'})


class EquipmentDelete(DeleteView):
    model = Permit
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        equipment = self.model.objects.get(id_com=id)
        alert_plate = Alert.objects.filter(
            category="Urgents",
            description="Expires of the Plate Equipment Number " + str(
                equipment.plate_account_number) + " of the customer " + str(equipment.customer))

        alert_reg = Alert.objects.filter(category="Urgents",
                                     description="Expires of the Title Register Equipment Number " + str(
                                         equipment.plate_account_number) + " of the customer " + str(equipment.customer))

        alert_insp = Alert.objects.filter(
            category="Urgents",
            description="Expires of the Inspection Equipment Number " + str(
                equipment.plate_account_number) + " of the customer " + str(equipment.customer))
        accion_user(equipment, DELETION, request.user)
        if alert_plate:
          alert_plate.delete()
        if alert_reg:
          alert_reg.delete()
        if alert_insp:
          alert_insp.delete()
        equipment.delete()
        messages.success(request, "Permit delete with an extension")
        return HttpResponseRedirect(self.success_url)

def InsuranceView(request, pk, popup):
    insurance = Insurance.objects.get(id_ins=pk)
    return render(request, 'services/insurance/insuranceView.html', {'insurance': insurance, 'is_popup':popup, 'title':'Insurance', 'deactivate':True})


class InsuranceCreate(CreateView):
      model = Insurance
      template_name = 'services/insurance/insuranceForm.html'
      form_class = InsuranceForm

      def get(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          customer = Customer.objects.filter(deactivated=False).order_by('company_name')
          form = self.form_class(initial=self.initial)
          return render(request, self.template_name, {'form': form, 'customers':customer, 'is_popup': popup, 'title': 'Create Insurance'})

      def post(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          form = self.form_class(request.POST)
          if form.is_valid():
                  insurance = form.save(commit=False)
                  if popup:
                    customer = Customer.objects.get(id_cut=id)
                  else:
                      customer = Customer.objects.get(id_cut=request.POST['customers'])
                  insurance.customers = customer
                  insurance.users = request.user
                  insurance.update = datetime.now().strftime("%Y-%m-%d")
                  insurance.save()
                  if request.POST.get('policy_alert', False) and len(request.POST['policy_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = insurance.policy_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the Insurance Policy  of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                  if request.POST.get('monthly_alert', False) and len(request.POST['monthlypay']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = insurance.monthlypay
                        dateShow = dateExp - timedelta(days=7)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "The next "+dateExp+" is the monthly insurance payment day of the customer" + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                  accion_user(insurance, ADDITION, request.user)
                  messages.success(request, 'The Insurance was saved successfully')
                  return HttpResponseRedirect('/accounting/customers/view/'+str(insurance.customers_id))
          else:
              for er in form.errors:
                  messages.error(request, "ERROR: " + er)
              return render(request, self.template_name, {'form': form, 'is_popup': popup,'title': 'Create Insurance'})


class InsuranceEdit(UpdateView):
    model = Insurance
    template_name = 'services/insurance/insuranceForm.html'
    form_class = InsuranceForm

    def get_context_data(self, **kwargs):
        context = super(InsuranceEdit, self).get_context_data(**kwargs)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        insurance = self.model.objects.get(id_ins=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=insurance)
        context['id'] = pk
        context['is_popup'] = popup
        context['title'] = 'Edit Insurance'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
        else:
            popup = 0
        insurance = self.model.objects.get(id_ins=pk)
        form = self.form_class(request.POST, instance=insurance)
        if form.is_valid():
                insurance = form.save(commit=False)
                insurance.update = datetime.now().strftime("%Y-%m-%d")
                insurance.users = request.user
                insurance.save()
                customer = Customer.objects.get(id_cut=insurance.customers_id)
                if request.POST.get('policy_alert', False) and len(request.POST['policy_date_exp']) != 0:
                   dateExp = insurance.policy_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the Insurance Policy  of the customer " + str(customer), category="Urgents")
                   if alert:
                      alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the Insurance Policy  of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(
                        description="Expires the Insurance Policy  of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        alert.delete()
                if request.POST.get('monthly_alert', False) and len(request.POST['monthlypay']) != 0:
                   dateExp = insurance.monthlypay
                   dateShow = dateExp - timedelta(days=7)
                   alert = Alert.objects.filter(description = "The next "+dateExp+" is the monthly insurance payment day of the customer" + str(customer), category="Urgents")
                   if alert:
                      alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="The next "+dateExp+" is the monthly insurance payment day of the customer" + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(
                        description="The next "+dateExp+" is the monthly insurance payment day of the customer" + str(customer),
                        category="Urgents")
                    if alert:
                        alert.delete()
                accion_user(insurance, CHANGE, request.user)
                messages.success(request, 'The Insurance was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(insurance.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name,
                          {'form': form,  'is_popup': popup, 'title': 'Edit Insurance'})

class InsuranceDelete(DeleteView):
    model = Insurance
    template_name = 'confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        insurance = self.model.objects.get(id_ins=id)
        alert_policy = Alert.objects.filter(description = "Expires the Insurance Policy  of the customer " + str(insurance.customers),
                                     end_date=insurance.policy_date_exp)
        alert_monthly = Alert.objects.filter(
            description="The next "+dateExp+" is the monthly insurance payment day of the customer" + str(customer),
            end_date=insurance.monthlypay)
        accion_user(insurance, DELETION, request.user)
        if alert_policy:
          alert_policy.delete()
        if alert_monthly:
          alert_monthly.delete()
        customer = insurance.customers
        insurance.delete()
        messages.success(request, "Insurance delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))

def DriverView(request, pk, popup):
    driver = Driver.objects.get(id_drv=pk)
    return render(request, 'services/driver/driverView.html', {'driver': driver, 'is_popup':popup, 'title':'Driver', 'deactivate':True})

class DriverCreate(CreateView):
      model = Driver
      template_name = 'services/driver/driverForm.html'
      form_class = DriverForm

      def get(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          customer = Customer.objects.filter(deactivated=False).order_by('company_name')
          form = self.form_class(initial=self.initial)
          return render(request, self.template_name, {'form': form, 'customers':customer, 'is_popup': popup, 'title': 'Create Driver'})

      def post(self, request, *args, **kwargs):
          if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
          else:
              popup = 0
          form = self.form_class(request.POST)
          if form.is_valid():
              driver_exist = Driver.objects.filter(name=request.POST['name'], license_numb=request.POST['license_numb'])
              if driver_exist:
                  messages.error(request, 'The driver already exists')
                  form = self.form_class(initial=self.initial)
                  return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create Driver'})
              else:
                  driver = form.save(commit=False)
                  if popup:
                    customer = Customer.objects.get(id_cut=id)
                  else:
                      customer = Customer.objects.get(id_cut=request.POST['customers'])
                  driver.customers = customer
                  driver.users = request.user
                  driver.update = datetime.now().strftime("%Y-%m-%d")
                  if driver.deactivate:
                      driver.deactivate_date = datetime.now().strftime("%Y-%m-%d")
                  else:
                      driver.deactivate_date = None
                  driver.save()
                  if request.POST.get('lic_alert', False) and len(request.POST['lic_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name= 'System Manager')
                        group_offic = Group.objects.get(name= 'Office Specialist')
                        dateExp = driver.lic_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the License Driver of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                  if request.POST.get('medicard_alert', False) and len(request.POST['medicard_date_exp']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        dateExp = driver.medicard_date_exp
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category = "Urgents",
                            description = "Expires the Medicard Driver of the customer " + str(customer),
                            create_date = datetime.now().strftime("%Y-%m-%d"),
                            show_date = dateShow.strftime("%Y-%m-%d"),
                            end_date = dateExp.strftime("%Y-%m-%d"),
                            users = request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                  if request.POST.get('drugtest_alert', False) and len(request.POST['drugtest_date_exp']) != 0:
                      group_admin = Group.objects.get(name='System Administrator')
                      group_manag = Group.objects.get(name='System Manager')
                      group_offic = Group.objects.get(name='Office Specialist')
                      dateExp = driver.drugtest_date_exp
                      dateShow = dateExp - timedelta(days=30)
                      alert = Alert.objects.create(
                          category="Urgents",
                          description="Expires the Drugtest Driver of the customer " + str(customer),
                          create_date=datetime.now().strftime("%Y-%m-%d"),
                          show_date=dateShow.strftime("%Y-%m-%d"),
                          end_date=dateExp.strftime("%Y-%m-%d"),
                          users=request.user)
                      alert.group.add(group_admin, group_manag, group_offic)
                  if request.POST.get('mbr_alert', False) and len(request.POST['mbr_date_exp']) != 0:
                      group_admin = Group.objects.get(name='System Administrator')
                      group_manag = Group.objects.get(name='System Manager')
                      group_offic = Group.objects.get(name='Office Specialist')
                      dateExp = driver.mbr_date_exp
                      dateShow = dateExp - timedelta(days=30)
                      alert = Alert.objects.create(
                          category="Urgents",
                          description="Expires the Mbr Driver of the customer " + str(customer),
                          create_date=datetime.now().strftime("%Y-%m-%d"),
                          show_date=dateShow.strftime("%Y-%m-%d"),
                          end_date=dateExp.strftime("%Y-%m-%d"),
                          users=request.user)
                      alert.group.add(group_admin, group_manag, group_offic)
                  accion_user(driver, ADDITION, request.user)
                  messages.success(request, 'The Driver was saved successfully')
                  return HttpResponseRedirect('/accounting/customers/view/'+str(driver.customers_id))
          else:
              for er in form.errors:
                  messages.error(request, "ERROR: " + er)
              return render(request, self.template_name, {'form': form, 'is_popup': popup,'title': 'Create Driver'})


class DriverEdit(UpdateView):
    model = Driver
    template_name = 'services/driver/driverForm.html'
    form_class = DriverForm

    def get_context_data(self, **kwargs):
        context = super(DriverEdit, self).get_context_data(**kwargs)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        driver = self.model.objects.get(id_drv=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=driver)
        context['id'] = pk
        context['is_popup'] = popup
        context['title'] = 'Edit Driver'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
        else:
            popup = 0
        driver = self.model.objects.get(id_drv=pk)
        form = self.form_class(request.POST, instance=driver)
        if form.is_valid():
                driver = form.save(commit=False)
                driver.update = datetime.now().strftime("%Y-%m-%d")
                driver.users = request.user
                driver.save()
                customer = Customer.objects.get(id_cut=driver.customers_id)

                if request.POST.get('lic_alert', False) and len(request.POST['lic_date_exp']) != 0:
                   dateExp = driver.lic_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the License Driver of the customer " + str(customer), category="Urgents")
                   if alert:
                      alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the License Driver of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(
                        description="Expires the License Driver of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        alert.delete()
                if request.POST.get('medicard_alert', False) and len(request.POST['medicard_date_exp']) != 0:
                   dateExp = driver.medicard_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the Medicard Driver of the customer " + str(customer), category="Urgents")
                   if alert:
                       alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the Medicard Driver of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(description="Expires the Medicard Driver of the customer " + str(customer), category="Urgents")
                    if alert:
                        alert.delete()
                if request.POST.get('drugtest_alert', False) and len(request.POST['drugtest_date_exp']) != 0:
                   dateExp = driver.drugtest_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the Drugtest Driver of the customer " + str(customer), category="Urgents")
                   if alert:
                       alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the Drugtest Driver of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(description="Expires the Drugtest Driver of the customer " + str(customer), category="Urgents")
                    if alert:
                        alert.delete()
                if request.POST.get('mbr_alert', False) and len(request.POST['mbr_date_exp']) != 0:
                   dateExp = driver.mbr_date_exp
                   dateShow = dateExp - timedelta(days=30)
                   alert = Alert.objects.filter(description = "Expires the Mbr Driver of the customer " + str(customer), category="Urgents")
                   if alert:
                       alert.update(show_date = dateShow.strftime("%Y-%m-%d"), end_date = dateExp.strftime("%Y-%m-%d"))
                   else:
                       group_admin = Group.objects.get(name='System Administrator')
                       group_manag = Group.objects.get(name='System Manager')
                       group_offic = Group.objects.get(name='Office Specialist')
                       alert = Alert.objects.create(
                           category="Urgents",
                           description="Expires the Mbr Driver of the customer " + str(customer),
                           create_date=datetime.now().strftime("%Y-%m-%d"),
                           show_date=dateShow.strftime("%Y-%m-%d"),
                           end_date=dateExp.strftime("%Y-%m-%d"),
                           users=request.user)
                       alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(description="Expires the Mbr Driver of the customer " + str(customer), category="Urgents")
                    if alert:
                        alert.delete()
                accion_user(driver, CHANGE, request.user)
                messages.success(request, 'The Driver was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(driver.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name,
                          {'form': form,  'is_popup': popup, 'title': 'Edit Driver'})

class DriverDelete(DeleteView):
    model = Driver
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        driver = self.model.objects.get(id_drv=id)
        alert_lic = Alert.objects.filter(description="Expires the License Driver of the customer " + str(driver.customers),
                                           end_date=driver.lic_date_exp)
        alert_medicard = Alert.objects.filter(description="Expires the Medicard Driver of the customer" + str(driver.customers),
                                           end_date=driver.medicard_date_exp)
        alert_drugtest = Alert.objects.filter(description="Expires the Drugtest Driver of the customer " + str(driver.customers),
                                           end_date=driver.drugtest_date_exp)
        alert_mbr = Alert.objects.filter(description="Expires the Mbr Driver of the customer" + str(driver.customers),
                                           end_date=driver.mbr_date_exp)
        accion_user(driver, DELETION, request.user)
        if alert_lic:
            alert_lic.delete()
        if alert_medicard:
            alert_medicard.delete()
        if alert_drugtest:
            alert_drugtest.delete()
        if alert_mbr:
            alert_mbr.delete()
        customer = driver.customers
        driver.delete()
        messages.success(request, "Driver delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))

def IftaView(request, pk, popup):
        ifta = Ifta.objects.get(id_ift=pk)
        return render(request, 'services/ifta/iftaView.html',
                      {'ifta': ifta, 'is_popup': popup, 'title': 'Ifta', 'deactivate': True})

class IftaCreate(CreateView):
        model = Ifta
        template_name = 'services/ifta/iftaForm.html'
        form_class = IftaForm

        def get(self, request, *args, **kwargs):
            if kwargs.__contains__('popup'):
                popup = kwargs['popup']
                id = kwargs['pk']
            else:
                popup = 0
            customer = Customer.objects.filter(deactivated=False).order_by('company_name')
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name,
                          {'form': form, 'customers': customer, 'is_popup': popup, 'title': 'Create Ifta'})

        def post(self, request, *args, **kwargs):
            if kwargs.__contains__('popup'):
                popup = kwargs['popup']
                id = kwargs['pk']
            else:
                popup = 0
            form = self.form_class(request.POST)
            if form.is_valid():
                    ifta = form.save(commit=False)
                    if popup:
                        customer = Customer.objects.get(id_cut=id)
                    else:
                        customer = Customer.objects.get(id_cut=request.POST['customers'])
                    ifta.customers = customer
                    ifta.users = request.user
                    ifta.update = datetime.now().strftime("%Y-%m-%d")
                    ifta.save()
                    if request.POST.get('nex_period_alert', False) and len(request.POST['nex_period']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        dateExp = ifta.nex_period
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="Next period of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                    if request.POST.get('payment_alert', False) and len(request.POST['payment_due']) != 0:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        dateExp = ifta.payment_due
                        dateShow = dateExp - timedelta(days=30)
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="IFTA Payment Due of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)

                    accion_user(ifta, ADDITION, request.user)
                    messages.success(request, 'The Ifta was saved successfully')
                    return HttpResponseRedirect('/accounting/customers/view/' + str(ifta.customers_id))
            else:
                for er in form.errors:
                    messages.error(request, "ERROR: " + er)
                return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create Ifta'})

class IftaEdit(UpdateView):
        model = Ifta
        template_name = 'services/ifta/iftaForm.html'
        form_class = IftaForm

        def get_context_data(self, **kwargs):
            context = super(IftaEdit, self).get_context_data(**kwargs)
            if self.kwargs.__contains__('popup'):
                popup = self.kwargs.get('popup')
            else:
                popup = 0
            pk = self.kwargs.get('pk', 0)
            ifta = self.model.objects.get(id_ift=pk)
            if 'form' not in context:
                context['form'] = self.form_class(instance=ifta)
            context['id'] = pk
            context['is_popup'] = popup
            context['title'] = 'Edit Ifta'
            return context

        def post(self, request, *args, **kwargs):
            self.object = self.get_object
            pk = kwargs['pk']
            if kwargs.__contains__('popup'):
                popup = kwargs['popup']
            else:
                popup = 0
            ifta = self.model.objects.get(id_ift=pk)
            form = self.form_class(request.POST, instance=ifta)
            if form.is_valid():
                ifta = form.save(commit=False)
                ifta.update = datetime.now().strftime("%Y-%m-%d")
                ifta.users = request.user
                ifta.save()
                customer = Customer.objects.get(id_cut=ifta.customers_id)
                if request.POST.get('nex_period_alert', False) and len(request.POST['nex_period']) != 0:
                    dateExp = ifta.nex_period
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.filter(
                        description="Next period of the customer " + str(customer), category="Urgents")
                    if alert:
                        alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                    else:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="Next period of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(
                        description="Next period of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        alert.delete()
                if request.POST.get('payment', False) and len(request.POST['payment_due']) != 0:
                    dateExp = ifta.payment_due
                    dateShow = dateExp - timedelta(days=30)
                    alert = Alert.objects.filter(
                        description="IFTA Payment Due of the customer " + str(customer), category="Urgents")
                    if alert:
                        alert.update(show_date=dateShow.strftime("%Y-%m-%d"), end_date=dateExp.strftime("%Y-%m-%d"))
                    else:
                        group_admin = Group.objects.get(name='System Administrator')
                        group_manag = Group.objects.get(name='System Manager')
                        group_offic = Group.objects.get(name='Office Specialist')
                        alert = Alert.objects.create(
                            category="Urgents",
                            description="IFTA Payment Due of the customer " + str(customer),
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            show_date=dateShow.strftime("%Y-%m-%d"),
                            end_date=dateExp.strftime("%Y-%m-%d"),
                            users=request.user)
                        alert.group.add(group_admin, group_manag, group_offic)
                else:
                    alert = Alert.objects.filter(
                        description="IFTA Payment Due of the customer " + str(customer),
                        category="Urgents")
                    if alert:
                        alert.delete()
                accion_user(ifta, CHANGE, request.user)
                messages.success(request, 'The Ifta was saved successfully')
                return HttpResponseRedirect('/accounting/customers/view/' + str(ifta.customers_id))
            else:
                for er in form.errors:
                    messages.error(request, "ERROR: " + er)
                return render(request, self.template_name,
                              {'form': form, 'is_popup': popup, 'title': 'Edit Ifta'})

class IftaDelete(DeleteView):
        model = Ifta
        template_name = 'confirm_delete.html'
        success_url = reverse_lazy('accounting:customer')

        def delete(self, request, *args, **kwargs):
            self.object = self.get_object
            id = kwargs['pk']
            ifta = self.model.objects.get(id_ift=id)
            nex_period_alert = Alert.objects.filter(
                description="Next period of the customer " + str(ifta.customers),
                end_date=ifta.nex_period)
            payment_alert = Alert.objects.filter(
                description="IFTA Payment Due of the customer " + str(ifta.customers),
                end_date=ifta.payment_due)
            accion_user(ifta, DELETION, request.user)
            if nex_period_alert:
                nex_period_alert.delete()
            if payment_alert:
                payment_alert.delete()
            customer = ifta.customers
            ifta.delete()
            messages.success(request, "Ifta delete with an extension")
            return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))

def AuditView(request, pk, popup):
    audit = Audit.objects.get(id_aud=pk)
    return render(request, 'services/audit/auditView.html',
                  {'audit': audit, 'is_popup': popup, 'title': 'Audit', 'deactivate': True})


class AuditCreate(CreateView):
    model = Audit
    template_name = 'services/audit/auditForm.html'
    form_class = AuditForm

    def get(self, request, *args, **kwargs):
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
        else:
            popup = 0
        customer = Customer.objects.filter(deactivated=False).order_by('company_name')
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form, 'customers': customer, 'is_popup': popup, 'title': 'Create Audit'})

    def post(self, request, *args, **kwargs):
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
            id = kwargs['pk']
        else:
            popup = 0
        form = self.form_class(request.POST)
        if form.is_valid():
            audit = form.save(commit=False)
            if popup:
                customer = Customer.objects.get(id_cut=id)
            else:
                customer = Customer.objects.get(id_cut=request.POST['customers'])
            audit.customers = customer
            audit.users = request.user
            audit.update = datetime.now().strftime("%Y-%m-%d")
            audit.save()
            accion_user(audit, ADDITION, request.user)
            messages.success(request, 'The Audit was saved successfully')
            return HttpResponseRedirect('/accounting/customers/view/' + str(audit.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'is_popup': popup, 'title': 'Create Audit'})


class AuditEdit(UpdateView):
    model = Audit
    template_name = 'services/audit/auditForm.html'
    form_class = AuditForm

    def get_context_data(self, **kwargs):
        context = super(AuditEdit, self).get_context_data(**kwargs)
        if self.kwargs.__contains__('popup'):
            popup = self.kwargs.get('popup')
        else:
            popup = 0
        pk = self.kwargs.get('pk', 0)
        audit = self.model.objects.get(id_aud=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=audit)
        context['id'] = pk
        context['is_popup'] = popup
        context['title'] = 'Edit Audit'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        if kwargs.__contains__('popup'):
            popup = kwargs['popup']
        else:
            popup = 0
        audit = self.model.objects.get(id_aud=pk)
        form = self.form_class(request.POST, instance=audit)
        if form.is_valid():
            audit = form.save(commit=False)
            audit.update = datetime.now().strftime("%Y-%m-%d")
            audit.users = request.user
            audit.save()
            accion_user(audit, CHANGE, request.user)
            messages.success(request, 'The Audit was saved successfully')
            return HttpResponseRedirect('/accounting/customers/view/' + str(audit.customers_id))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name,
                          {'form': form, 'is_popup': popup, 'title': 'Edit Audit'})


class AuditDelete(DeleteView):
    model = Audit
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('accounting:customer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        audit = self.model.objects.get(id_aud=id)
        accion_user(audit, DELETION, request.user)
        customer = audit.customers
        audit.delete()
        messages.success(request, "Audit delete with an extension")
        return HttpResponseRedirect('/accounting/customers/view/' + str(customer.id_cut))