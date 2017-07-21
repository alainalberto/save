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
from apps.tools.components.DirectoryForm import DirectoryForm
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from datetime import datetime, date, time, timedelta
from django.core.mail import send_mail
from twilio.rest import Client
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

# Create your views here.

def Chats(request):
    return render(request, "home/complement/chat.html")

class DirectoryTelephone(ListView):
    model = Directory
    template_name = 'directorytelephone/directoryViews.html'


class DirectoryTelephoneCreate(CreateView):
    model = Directory
    form_class = DirectoryForm
    template_name = 'directorytelephone/directoryForm.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'title': 'Create new Directory'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user
        if form.is_valid():
            alert = form.save(commit=False)
            alert.users = user
            alert.save()
            accion_user(alert, ADDITION, request.user)
            messages.success(request, "Contact save")

        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'title': 'Create New Contact'})
        return HttpResponseRedirect(reverse_lazy('panel:directory'))

class DirectoryTelephoneEdit(UpdateView):
    model = Directory
    form_class = DirectoryForm
    template_name = 'directorytelephone/directoryForm.html'
    success_url = reverse_lazy('panel:directory')


    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dir = kwargs['pk']
        directory = self.model.objects.get(id_dir=id_dir)
        form = self.form_class(request.POST, instance=directory)
        if form.is_valid():
            directory =form.save()
            accion_user(directory, CHANGE, request.user)
            messages.success(request, "Contact update")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Contact'})

class DirectoryTelephoneDelete(DeleteView):
    model = Directory
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('panel:directory')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_dir = kwargs['pk']
        directory = self.model.objects.get(id_dir=id_dir)
        accion_user(directory, DELETION, request.user)
        directory.delete()
        messages.success(request, "Contact delete")
        return HttpResponseRedirect(self.success_url)

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(users=request.user, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': c.users.username})
    else:
        return HttpResponse('Request must be POST.')

def Message(request):
    c = Chat.objects.all()
    return render(request, 'home/complement/messages.html', {'chat': c})

def panel_view(request):
    balance = []
    income = []
    valueInc = 0
    valueExp = 0
    alertUrg = Alert.objects.filter(category='Urgents')
    date_now = datetime.now().date()
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


    contexto = {'balance': balance, 'alert':alertUrg, 'date_now':date_now}
    return render(request, 'home/complement/panel.html', contexto)

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
            accion_user(calendar, ADDITION, request.user)
            messages.success(request, 'Event saved with an extension')
            return HttpResponseRedirect(reverse_lazy('panel:calendar'))
        else:
            for er in form.errors:
                messages.error(request, "ERROR: " + er)
            return render(request, self.template_name, {'form': form, 'title': 'Create new Event'})

class UpdateCalendar(UpdateView):
    model = Calendar
    form_class = CalendarForm.CalendarForm
    template_name = 'home/calendar/calendarForm.html'
    success_url = reverse_lazy('panel:calendar')

    def get_context_data(self, **kwargs):
        context = super(UpdateCalendar, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        event = self.model.objects.get(id=pk)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['id'] = pk
        context['event'] = event
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cal = kwargs['pk']
        calendar = self.model.objects.get(id=id_cal)
        form = self.form_class(request.POST, instance=calendar)
        if form.is_valid():
            calendar =form.save()
            accion_user(calendar, CHANGE, request.user)
            messages.success(request, "Event update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit new Event'})

class DeleteCalendar(DeleteView):
    model = Calendar
    form_class = CalendarForm.CalendarForm
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('panel:calendar')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cal = kwargs['pk']
        calendar = self.model.objects.get(id=id_cal)
        accion_user(calendar, DELETION, request.user)
        calendar.delete()
        messages.success(request, "Enent delete with an extension")
        return HttpResponseRedirect(self.success_url)

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
    notifications = Alert.objects.filter(category='Notification')
    contexto = {'alerts': notifications, 'title':'List Notification', 'style':'success'}
    return render(requiret, 'alert/alertViews.html', contexto)

def AlertView(requiret):
    alertas = Alert.objects.filter(category='Alerts')
    contexto = {'alerts': alertas, 'title':'List Alert', 'style':'warning'}
    return render(requiret, 'alert/alertViews.html', contexto)

def UrgentView(requiret):
    urgents = Alert.objects.filter(category='Urgents')
    contexto = {'alerts': urgents, 'title':'List Urgent', 'style':'danger'}
    return render(requiret, 'alert/alertViews.html', contexto)

def AllalertView(requiret):
    allalert = Alert.objects.all().order_by('-category')
    contexto = {'alerts': allalert, 'title':'List All Alerts', 'style':'primary'}
    return render(requiret, 'alert/alertViews.html', contexto)

class AlertsCreate(CreateView):
     model = Alert
     form_class = AlertForm
     template_name = 'alert/alertForm.html'

     def get(self, request, *args, **kwargs):
         form = self.form_class(initial=self.initial)
         return render(request, self.template_name, {'form': form, 'title': 'Create new Alert'})

     def post(self, request, *args, **kwargs):
         form = self.form_class(request.POST)
         user = request.user
         if form.is_valid():
             alert = form.save(commit=False)
             alert.users = user
             alert.save()
             accion_user(alert, ADDITION, request.user)
             messages.success(request, "Alert save with an extension")
             send_mail(
                 'FirstCall Alert',
                 'Usted tiene una alerta:'+ alert.description + ' con fecha de terminación ' +str(alert.end_date),
                 'ranselr@gmail.com',
                 ['ranselr@gmail.com'],
                 fail_silently=False,
             )
             # Your Account SID from twilio.com/console
             account_sid = "ACc2b4aa7154629a3f9b2767e7ddf9981d"
             # Your Auth Token from twilio.com/console
             auth_token = "b6318ebc29ac5cbdc257bb9acac2d89c"

             client = Client(account_sid, auth_token)

             message = client.messages.create(
                 to="+18322071590",
                 from_="+18329002832",
                 body="Hello my wife!")

         else:
             for er in form.errors:
                 messages.error(request, "ERROR: " + er)
             return render(request, self.template_name, {'form': form, 'title': 'Create new Alert'})
         return HttpResponseRedirect(reverse_lazy('panel:panel'))


class AlertstEdit(UpdateView):
    model = Alert
    form_class = AlertForm
    template_name = 'alert/alertForm.html'
    success_url = reverse_lazy('panel:allalert')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_alt = kwargs['pk']
        alert = self.model.objects.get(id_alt=id_alt)
        form = self.form_class(request.POST, instance=alert)
        if form.is_valid():
            alert =form.save()
            accion_user(alert, CHANGE, request.user)
            messages.success(request, "Alert update with an extension")
            return HttpResponseRedirect(self.success_url)
        else:
            for er in form.errors:
                messages.error(request, "ERROR: "+er)
            return render(request, self.template_name, {'form': form, 'title': 'Edit Alert'})

class AlertsDelete(DeleteView):
    model = Alert
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('panel:allalert')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object
        id_alt = kwargs['pk']
        alert = self.model.objects.get(id_alt=id_alt)
        accion_user(alert, DELETION, request.user)
        alert.delete()
        messages.success(request, "Enent delete with an extension")
        return HttpResponseRedirect(self.success_url)

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
