from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic import TemplateView
from apps.tools.models import Menu, Alert


def home_view(requiret):
    menus = Menu.objects.filter(menus_id=None)
    submenus = Menu.objects.filter()
    alertNot = Alert.objects.filter(category='Notification')
    alertAlt = Alert.objects.filter(category='Alert')
    alertUrg = Alert.objects.filter(category='Urgent')
    contexto = {'menus': menus, 'submenus': submenus, 'notif': alertNot.count(),
                'alert': alertAlt.count(), 'urgent': alertUrg.count()}
    return render(requiret, 'home/complement/panel.html', contexto)
