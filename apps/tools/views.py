from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, View, TemplateView
from apps.tools.models import *
from apps.tools.components import CalendarForm, AlertForm
from apps.tools.components.AlertForm import AlertForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages




# Create your views here.

def home_view(requiret):
    alertNot = Alert.objects.filter(category='Notification')
    alertAlt = Alert.objects.filter(category='Alerts')
    alertUrg = Alert.objects.filter(category='Urgents')
    allalert = alertNot.count() + alertAlt.count() + alertUrg.count()
    contexto = {'notif': alertNot.count(),'alert': alertAlt.count(), 'urgent': alertUrg.count(), 'allalert': allalert}
    return render(requiret, 'home/complement/panel.html', contexto)


def panel_view(requiret):
    alertNot = Alert.objects.filter(category='Notification')
    alertAlt = Alert.objects.filter(category='Alerts')
    alertUrg = Alert.objects.filter(category='Urgents')
    allalert = alertNot.count() + alertAlt.count() + alertUrg.count()
    contexto = {'notif': alertNot.count(), 'alert': alertAlt.count(), 'urgent': alertUrg.count(), 'allalert': allalert}
    return render(requiret, 'home/complement/panel.html', contexto)

class PostCalendar(CreateView):
    model = Calendar
    form_class = CalendarForm.CalendarForm
    template_name = 'home/calendar/calendarForm.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.users_id = user.id
            calendar.save()
            return HttpResponseRedirect(reverse_lazy('panel:calendar'))

class UpdateCalendar(UpdateView):
    model = Calendar
    form_class = CalendarForm.CalendarForm
    template_name = 'home/calendar/calendarForm.html'
    success_url = reverse_lazy('panel:calendar')

class DeleteCalendar(DeleteView):
    model = Calendar
    form_class = CalendarForm.CalendarForm
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('panel:calendar')

class Calendar_Panel(TemplateView):
    template_name = 'home/calendar/calendar_panel.html'


def GetCalendar(requiret):
    calendar = Calendar.objects.filter(users=requiret.user.id)
    event_json = []
    for event in calendar:
        events_user = {}
        events_user['start'] = str(event.start) + "T" + str(event.startTimer)
        events_user['end'] = str(event.end) + "T" + str(event.endTimer)
        events_user['title'] = event.title
        events_user['color'] = event.color
        events_user['url'] = "/panel/calendar/edit/"+str(event.id)
        if event.allDay:
           events_user['allDay'] = 'true'
        else:
           events_user['allDay'] = 'false'
        event_json.append(events_user)
    context = event_json
    return JsonResponse(context, safe=False)

#Alert
def NotificationView(requiret):
    grupos = Group.objects.get(user=requiret.user)
    notifications = Alert.objects.all()
    contexto = {'notifications': notifications, 'grupos': grupos}
    return render(requiret, 'alert/notificationViews.html', contexto)

def AlertView(requiret):
    grupos = Group.objects.get(user=requiret.user)
    alertas = Alert.objects.all()
    contexto = {'alertas': alertas, 'grupos': grupos}
    return render(requiret, 'alert/alertViews.html', contexto)

def UrgentView(requiret):
    grupos = Group.objects.get(user=requiret.user)
    urgents = Alert.objects.all()
    contexto = {'urgents': urgents, 'grupos': grupos}
    return render(requiret, 'alert/urgentViews.html', contexto)

class AlertsCreate(CreateView):
     model = Alert
     form_class = AlertForm
     template_name = 'alert/alertForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form})

     def post(self, request, *args, **kwargs):
         form = self.form_class(request.POST)
         user = request.user
         if form.is_valid():
             alert = form.save(commit=False)
             alert.users = user
             alert.save()
         return HttpResponseRedirect(reverse_lazy('panel:panel'))


class AlertstEdit(UpdateView):
    model = Alert
    form_class = AlertForm
    template_name = 'alert/alertForm.html'
    success_url = reverse_lazy('panel:panel')

class AlertsDelete(DeleteView):
    model = Alert
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('panel:panel')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Login/change_password.html', {
        'form': form
    })
