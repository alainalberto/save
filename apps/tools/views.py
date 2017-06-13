from django.core.mail.backends import console
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.shortcuts import render, render_to_response, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from FirstCall.util import accion_user
from apps.accounting.models import AccountDescrip, Account
from apps.tools.models import *
from apps.tools.components import CalendarForm, AlertForm
from apps.tools.components.AlertForm import AlertForm
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
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

    balance = []
    income = []
    valueInc = 0
    valueExp = 0
    inc = Account.objects.get(primary=True, name='Income')
    inc_acconts = Account.objects.filter(accounts_id_id=inc.id_acn)
    for i in inc_acconts:
        income.append(i)
    for a in inc_acconts:
        inc_accont = Account.objects.filter(accounts_id_id=a.id_acn)
        if inc_accont != None:
            for ac in inc_accont:
                income.append(ac)
    expense = []
    exp = Account.objects.get(primary=True, name='Expenses')
    exp_acconts = Account.objects.filter(accounts_id_id=exp.id_acn)
    for e in exp_acconts:
        expense.append(e)
    for a in exp_acconts:
        exp_accont = Account.objects.filter(accounts_id_id=a.id_acn)
        if exp_accont != None:
            for ac in exp_accont:
                expense.append(ac)
    accounts = Account.objects.filter(primary=False)
    for a in accounts:
        if income.__contains__('a.name') and expense.__contains__('a.name'):
            for e in expense:
                if e.name == a.name:
                    Exp = AccountDescrip.objects.filter(accounts_id=e.id_acn)
                    for sum in Exp:
                        valueExp = valueExp + int(sum.value)
            for i in income:
                if i.name == a.name:
                    Inc = AccountDescrip.objects.filter(accounts_id=i.id_acn)
                    for sum in Inc:
                        valueInc = valueInc + int(sum.value)
            valueEarn = valueInc - int(valueExp)
            balance.append({'account': e.name, 'income': valueInc, 'expense': valueExp, 'earning': str(valueEarn)})
        if income.__contains__('a.name') and not expense.__contains__('a.name'):
            for i in income:
                if i.name == a.name:
                    Inc = AccountDescrip.objects.filter(accounts_id=i.id_acn)
                    for sum in Inc:
                        valueInc = valueInc + int(sum.value)
            valueEarn = valueInc - int(valueExp)
            balance.append({'account': e.name, 'income': valueInc, 'expense': valueExp, 'earning': str(valueEarn)})
        if not income.__contains__('a.name') and expense.__contains__('a.name'):
            for e in expense:
                if e.name == a.name:
                    Exp = AccountDescrip.objects.filter(accounts_id=e.id_acn)
                    for sum in Exp:
                        valueExp = valueExp + int(sum.value)
            valueEarn = valueInc - int(valueExp)
            balance.append({'account': e.name, 'income': valueInc, 'expense': valueExp, 'earning': str(valueEarn)})


    alertNot = Alert.objects.filter(category='Notification')
    alertAlt = Alert.objects.filter(category='Alerts')
    alertUrg = Alert.objects.filter(category='Urgents')
    allalert = alertNot.count() + alertAlt.count() + alertUrg.count()
    contexto = {'notif': alertNot.count(), 'alert': alertAlt.count(), 'urgent': alertUrg.count(), 'allalert': allalert, 'balance': balance}
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

def AllalertView(requiret):
    grupos = Group.objects.get(user=requiret.user)
    #Reserved.objects.filter(client=client_id).order_by('-check_in')
    allalert = Alert.objects.all().order_by('-category')
    contexto = {'allalert': allalert, 'grupos': grupos}
    return render(requiret, 'alert/allalertViews.html', contexto)

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
             accion_user(alert, ADDITION, request.user)
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
