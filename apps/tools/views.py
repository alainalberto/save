from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from apps.tools.models import *
from apps.tools.components import CalendarForm, alertForm
from django.contrib.auth import authenticate, logout, login
import simplejson


from apps.tools.components.chatForm import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# Create your views here.

class PostCalendar(CreateView):
    model = Calendar
    form_class = CalendarForm.CalendarForm
    template_name = 'home/calendar/calendarForm.html'
    success_url = reverse_lazy('panel:calendar')

def panel_view(requiret):
    form = chatForm
    return render(requiret, 'home/complement/panel.html', {'panel': 'active'})

def Calendar_Panel(requiret):
    return render(requiret, 'home/calendar/calendar_panel.html')

def GetCalendar(requiret):
    calendar = Calendar.objects.filter(users=requiret.user.id)
    event_json = []
    for event in calendar:
        events_user = {}
        events_user['title'] = event.title
        events_user['color'] = event.color
        events_user['allDay'] = event.allDay
        events_user['start'] = event.start + "T" + event.startTimer
        events_user['end'] = event.end + "T" + event.endTimer
        event_json.append(events_user)
    response_data = simplejson.dumps(event_json)
    return JsonResponse(response_data)

#Alert
def NotificationView(requiret):
    #grupos = requiret.user.groups.all
    #pepe = User.objects.filter(groups__name='Familia')
    notification = Alert.objects.filter(category='Notification')
    #e = Group.objects.filter(user=requiret.user)
    grupos = Group.objects.get(id=requiret.user.id)
    e = grupos.alert_set.filter(category='Notification')
    contexto = {'notification': notification, 'e': e}
    return render(requiret, 'alert/notificationViews.html', contexto)

def AlertView(requiret):
    alert = Alert.objects.filter(category='Alerts')
    contexto = {'alerts': alert}
    return render(requiret, 'alert/alertViews.html', contexto)

def UrgentView(requiret):
    urgent = Alert.objects.filter(category='Urgents')
    contexto = {'urgents': urgent}
    return render(requiret, 'alert/urgentViews.html', contexto)

class AlertsCreate(CreateView):
     model = Alert
     form_class = alertForm
     template_name = 'alert/alertForm.html'

     def post(self, request, args, *kwargs):
         self.object = self.get_object()
         form = self.form_class(request.POST)
         user = request.user
         if form.is_valid():
             alert = form.save(commit=False)
             alert.users = user
             alert.save()
             return HttpResponseRedirect(reverse_lazy('panel'))

class AlertstEdit(UpdateView):
    model = Alert
    form_class = alertForm
    template_name = 'alert/alertForm.html'
    success_url = reverse_lazy('panel')

class AlertsDelete(DeleteView):
    model = Alert
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('panel')

