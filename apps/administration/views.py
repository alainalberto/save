from django.shortcuts import render

from django.utils import timezone

from apps.administration.models import Menus, Users, Alerts


# Create your views here.
def signin(request):
    return render(request, 'layout/signin.html')


def home_wiew(request):
      menus = Menus.objects.all()
      user = Users.objects.filter(id_use=1)
      alertNot = Alerts.objects.filter(category='Notification')
      alertAlt = Alerts.objects.filter(category='Alert')
      alertUrg = Alerts.objects.filter(category='Urgent')
      contexto = {'menus' : menus,'user': user,'notif' : alertNot.count(),'alert' : alertAlt.count(),'urgent' : alertUrg.count()}
      return render(request, 'administration/complement/panel.html', {'menus' : menus,'user': user,'notif' : alertNot,'alert' : alertAlt,'urgent' : alertUrg})
