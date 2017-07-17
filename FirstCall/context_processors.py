from apps.tools.models import *
from django.contrib.auth.models import User, Group
from datetime import datetime, date, time, timedelta


def base(request):
    date_now = datetime.now().date()
    notif = []
    alert = []
    urgent = []
    alertNot = Alert.objects.filter(category='Notification')
    alertAlt = Alert.objects.filter(category='Alerts')
    alertUrg = Alert.objects.filter(category='Urgents')
    for n in alertNot:
        if n.show_date <= date_now and n.end_date >= date_now:
           notif.append(n)
    for a in alertAlt:
        if a.show_date <= date_now and a.end_date >= date_now:
           alert.append(a)
    for u in alertUrg:
        if u.show_date <= date_now and u.end_date >= date_now:
           urgent.append(u)
    all = len(notif) + len(alert) + len(urgent)
    c = Chat.objects.all()
    contexto = {'notif': len(notif), 'alrt': len(alert), 'urgent': len(urgent), 'all': all, 'chat': c}
    return (contexto)