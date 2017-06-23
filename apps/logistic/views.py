from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from apps.logistic.components.LogisticForm import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from FirstCall.util import accion_user
from apps.logistic.models import *


# Create your views here.


# Customers
class LoadsView(ListView):
    model = Load
    template_name = 'logistic/load/loadViews.html'

class LoadsCreate(CreateView):
     model = Load
     form_class = LoadsForm
     template_name = 'logistic/load/loadForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Load'})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         if form.is_valid():
             load_exist = Load.objects.filter(broker=form.data['broker'], number=form.data['number'])
             if load_exist:
                 messages.error(request, 'The load already exists')
                 form = self.form_class(initial=self.initial)
                 return render(request, self.template_name, {'form': form, 'title': 'Create new Drivers'})
             else:
                load = form.save(commit=False)
                load.users_id = user.id
                load.save()
                accion_user(load, ADDITION, request.user)
                messages.success(request, 'Load save with an extension')
                return HttpResponseRedirect(reverse_lazy('logistic:loads'))
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)

class LoadsEdit(UpdateView):
    model = Load
    form_class = LoadsForm
    template_name = 'logistic/load/loadForm.html'
    success_url = reverse_lazy('logistic:loads')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_lod = kwargs['pk']
        load = self.model.objects.get(id_lod=id_lod)
        form = self.form_class(request.POST, instance=load)
        if form.is_valid():
            load =form.save()
            accion_user(load, CHANGE, request.user)
            messages.success(request, "Load update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Load'})

class LoadsDelete(DeleteView):
    model = Load
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('logistic:loads')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_lod = kwargs['pk']
        load = self.model.objects.get(id_lod=id_lod)
        accion_user(load, DELETION, request.user)
        load.delete()
        messages.success(request, "Load delete with an extension")
        return HttpResponseRedirect(self.success_url)


#Drivers

class DriversView(ListView):
    model = DriversLogt
    template_name = 'logistic/drivers/driversViews.html'

class DriversCreate(CreateView):
     model = DriversLogt
     form_class = DriversForm
     template_name = 'logistic/drivers/driversForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Drivers'})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         if form.is_valid():
             driver_exist = DriversLogt.objects.filter(license_numb=form.data['license_numb'], name=form.data['name'])
             if driver_exist:
                 messages.error(request, 'The driver already exists')
                 form = self.form_class(initial=self.initial)
                 return render(request, self.template_name, {'form': form, 'title': 'Create new Drivers'})
             else:
                driver = form.save(commit=False)
                driver.users_id = user.id
                driver.save()
                accion_user(driver, ADDITION, request.user)
                messages.success(request, 'Driver save with an extension')
                return HttpResponseRedirect(reverse_lazy('logistic:drivers'))
         else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)

class DriversEdit(UpdateView):
    model = DriversLogt
    form_class = DriversForm
    template_name = 'logistic/drivers/driversForm.html'
    success_url = reverse_lazy('logistic:drivers')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dr = kwargs['pk']
        driver = self.model.objects.get(id_dr=id_dr)
        form = self.form_class(request.POST, instance=driver)
        if form.is_valid():
            driver =form.save()
            accion_user(driver, CHANGE, request.user)
            messages.success(request, "Driver update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Drivers'})


class DriversDelete(DeleteView):
    model = DriversLogt
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('logistic:drivers')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dr = kwargs['pk']
        driver = self.model.objects.get(id_dr=id_dr)
        accion_user(driver, DELETION, request.user)
        driver.delete()
        messages.success(request, "Driver delete with an extension")
        return HttpResponseRedirect(self.success_url)


#Distpacher

class DispatchView(ListView):
    model = DispatchLogt
    template_name = 'logistic/dispatch/dispatchViews.html'

class DispatchCreate(CreateView):
     model = DispatchLogt
     form_class = DispatchForm
     template_name = 'logistic/dispatch/dispatchForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Dispatch'})

     def post(self, request, *args, **kwargs):
         user = request.user
         form = self.form_class(request.POST)
         if form.is_valid():
             disp_exist = DispatchLogt.objects.filter(name=form.data['name'])
             if disp_exist:
                 messages.error(request, 'The dispatch already exists')
                 form = self.form_class(initial=self.initial)
                 return render(request, self.template_name, {'form': form, 'title': 'Create new Dispatch'})
             else:
                 disp = form.save(commit=False)
                 disp.users_id = user.id
                 disp.save()
                 accion_user(disp, ADDITION, request.user)
                 messages.success(request, "Dispatch save with an extension")
             return HttpResponseRedirect(reverse_lazy('logistic:dispatch'))
         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)
             return render(request, self.template_name, {'form': form, 'title': 'Edit Dispatch'})

class DispatchEdit(UpdateView):
    model = DispatchLogt
    form_class = DispatchForm
    template_name = 'logistic/dispatch/dispatchForm.html'
    success_url = reverse_lazy('logistic:dispatch')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dsp = kwargs['pk']
        disp = self.model.objects.get(id_dsp=id_dsp)
        form = self.form_class(request.POST, instance=disp)
        if form.is_valid():
            disp =form.save()
            accion_user(disp, CHANGE, request.user)
            messages.success(request, "Dispatch update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)


class DispatchDelete(DeleteView):
    model = DispatchLogt
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('logistic:dispatch')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dsp = kwargs['pk']
        disp = self.model.objects.get(id_dsp=id_dsp)
        accion_user(disp, DELETION, request.user)
        disp.delete()
        messages.success(request, "Dispatch delete with an extension")
        return HttpResponseRedirect(self.success_url)