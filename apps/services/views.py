from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from apps.logistic.models import Load
from apps.services.components.ServicesForm import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from apps.services.models import *
from apps.tools.models import Folder, Busines


# Create your views here.

class CompanyView(ListView):
    model = Companie
    template_name = 'accounting/receipts/receiptsViews.html'