from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from apps.logistic.models import Load
from apps.services.components.ServicesForm import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from apps.services.models import *
from apps.tools.models import Folder, Busines, File
from datetime import datetime, date, time, timedelta
from django.contrib import messages
from FirstCall.util import accion_user

# Create your views here.

class CompanyView(ListView):
    model = Companie
    template_name = 'accounting/receipts/receiptsViews.html'

class FileView(ListView):
    model = File
    template_name = 'services/file/fileViews.html'

class FileCreate(CreateView):
    model = File
    form_class = FileForm
    template_name = 'services/file/fileForm.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'title': 'Create new file'})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST , request.FILES)
        if form.is_valid():
           file = form.save(commit=False)
           file.users_id = user.id
           file.folders_id = 1
           date_now = datetime.today()
           formatDate = "%Y-%m-%d"
           file.date_save = date_now.strftime(formatDate)
           file.save()
           messages.success(request,"File saved with an extension")
           accion_user(file, ADDITION, request.user)
           return HttpResponseRedirect(reverse_lazy('services:forms'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)

class FileEdit(UpdateView):
    model = File
    form_class = FileForm
    template_name = 'services/file/fileForm.html'
    success_url = reverse_lazy('services:forms')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_fil = kwargs['pk']
        file = self.model.objects.get(id_fil=id_fil)
        form = self.form_class(request.POST, instance=file)
        if form.is_valid():
            file =form.save()
            accion_user(file, CHANGE, request.user)
            messages.success(request, "File update with an extension")
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
        messages.success(request, "File delete with an extension")
        return HttpResponseRedirect(self.success_url)