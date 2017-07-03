from apps.tools.models import *
from django.contrib.auth.models import User, Group


def base(request):
    notif = 0
    alert = 0
    urgent = 0
    all = 0
    alertNot = Alert.objects.filter(category='Notification')
    alertAlt = Alert.objects.filter(category='Alerts')
    alertUrg = Alert.objects.filter(category='Urgents')
    notif = alertNot.count()
    alert = alertAlt.count()
    urgent = alertUrg.count()
    all = alertNot.count() + alertAlt.count() + alertUrg.count()

    contexto = {'notif': notif , 'alert': alert, 'urgent': urgent, 'all': all}
    return (contexto)