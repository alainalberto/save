from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic import TemplateView
from apps.tools.models import Menu, Alert, Chat


def home_view(requiret):
    alertNot = Alert.objects.filter(category='Notification')
    alertAlt = Alert.objects.filter(category='Alerts')
    alertUrg = Alert.objects.filter(category='Urgents')
    allalert = alertNot.count() + alertAlt.count() + alertUrg.count()
    contexto = {'notif': alertNot.count(),'alert': alertAlt.count(), 'urgent': alertUrg.count(), 'allalert': allalert}
    return render(requiret, 'home/complement/panel.html', contexto)

def Chats(request):
    c = Chat.objects.all()
    return render(request, "home/complement/chat.html", {'chat': 'active', 'chat': c})

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(users=request.user, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': c.user.username})
    else:
        return HttpResponse('Request must be POST.')

def Messages(request):
    c = Chat.objects.all()
    return render(request, 'home/complement/messages.html', {'chat': c})