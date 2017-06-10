from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from apps.tools.models import Alert, Chat
#{% if request.user.id == c.users_id and c.category == 'Notification' or grupos.id == c.group.id and c.category == 'Notification' %}
        #            {% if c.deactivated == 0 %}

def home_view(requiret):
    alertNot = Alert.objects.filter(category='Notification', users=requiret.user.id)
    alertAlt = Alert.objects.filter(category='Alerts')
    alertUrg = Alert.objects.filter(category='Urgents')
    allalert = alertNot.count() + alertAlt.count() + alertUrg.count()
    contexto = {'notif': alertNot.count(),'alert': alertAlt.count(), 'urgent': alertUrg.count(), 'allalerts': allalert}
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

def Messages(request):
    c = Chat.objects.all()
    return render(request, 'home/complement/messages.html', {'chat': c})