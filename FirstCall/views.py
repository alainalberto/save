from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic import TemplateView
from apps.tools.models import Menu, Alert, Chat
from django.db.models import Q
from django.conf import settings
from django.template import Context
from django.template import RequestContext

def home_view(requiret):
    grupos = Group.objects.get(user=requiret.user)
    notification1 = Alert.objects.filter(Q(users=requiret.user, category='Notification', deactivated=0) | Q(group=grupos.id, category='Notification', deactivated=0))
    alertas1 = Alert.objects.filter(Q(users=requiret.user, category='Alerts', deactivated=0) | Q(group=grupos.id, category='Alerts', deactivated=0))
    urgents1 = Alert.objects.filter(Q(users=requiret.user, category='Urgents', deactivated=0) | Q(group=grupos.id, category='Urgents', deactivated=0))
    allalert1 = notification1.count() + alertas1.count() + urgents1.count()
    contexto = {'notification1': notification1, 'alertas1': alertas1, 'urgents1': urgents1, 'allalert1': allalert1}
    return render(requiret, 'home/complement/panel.html', contexto)

def Chats(request):
    c = Chat.objects.all()
    return render(request, "home/complement/chat.html", {'chat': c})

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(users=request.user, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': c.user.username})
    else:
        return HttpResponse('Request must be POST.')

def Message(request):
    c = Chat.objects.all()
    return render(request, 'home/complement/messages.html', {'chat': c})