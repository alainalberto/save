from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
from apps.accounting.models import Accounts, AccountDescrip
from apps.accounting.components.AccountingForm import AccountForm


# Create your views here.


class AccountingPanel(ListView):
    model = Accounts
    template_name = 'accounting/panel_account.html'


class AccountCreate(CreateView):
    model = Accounts
    form_class = AccountForm
    template_name = 'accounting/accounts/accountsForm.html'
    success_url = 'accounting:accounts'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Accounts.objects.create(name = self.request.POST["name"], description = self.request.POST["description"], accounts_id_id = self.request.POST["accounts_id"], users_id = user.id, primary = None)

def AccountsViews(requiret):
    primary = Accounts.objects.filter(primary=1)
    lisexp = Accounts.objects.filter(primary=None)
    contexto = {'accounts': lisexp, 'primary': primary}
    return render(requiret, 'accounting/accounts/accountsViews.html', contexto)


class AccountsDescViews(ListView):
    model = AccountDescrip.objects.filter()
    template_name = 'accounting/accounts/accountsDescrp.html'

