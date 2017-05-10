from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView
from apps.tools.models import Menus, Alerts


# Create your views here.

def home_view(request):
      menus = Menus.objects.filter(menus_id=None)
      submenus = Menus.objects.filter()
      user = User.objects.filter(id=1)
      alertNot = Alerts.objects.filter(category='Notification')
      alertAlt = Alerts.objects.filter(category='Alert')
      alertUrg = Alerts.objects.filter(category='Urgent')
      contexto = {'menus' : menus,'submenus': submenus, 'user': user,'notif': alertNot.count(),'alert' : alertAlt.count(),'urgent' : alertUrg.count()}
      return render(request, 'home/complement/panel.html', contexto)



