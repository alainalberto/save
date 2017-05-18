from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from apps.tools.models import *


# Create your views here.

def panel_view(requiret):
    return render(requiret, 'home/complement/panel.html')

def Calendar_Panel(requiret):
    events = Calendar.objects.filter()
    return render(requiret, 'home/calendar/calendar_panel.html')

