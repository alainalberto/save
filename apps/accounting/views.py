from django.shortcuts import render
from django.views.generic import ListView
from apps.accounting.models import Accounts, AccountDescrip
# Create your views here.


class AccountingPanel(ListView):
    model = Accounts
    template_name = 'accounting/panel_account.html'

def AccountsViews(requiret):
    primary = Accounts.objects.filter(primary=1)
    lisexp = Accounts.objects.filter(primary=None)
    contexto = {'accounts': lisexp,  'primary': primary}
    return render(requiret, 'accounting/accounts/accountsViews.html', contexto)

def AccountsDescViews(requiret, id):
    lisDesc = AccountDescrip.objects.filter(accounts_id=id)
    contexto = {'accounts': lisDesc}
    return render(requiret, 'accounting/accounts/accountsViews.html', contexto)