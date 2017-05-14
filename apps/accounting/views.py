from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from apps.accounting.models import Accounts, AccountDescrip, Customers
from apps.accounting.components.AccountingForm import AccountForm, CustomerForm


# Create your views here.


class AccountingPanel(ListView):
    model = Accounts
    template_name = 'accounting/panel_account.html'

class CustomersView(ListView):
    model = Customers
    template_name = 'accounting/customer/customerViews.html'

class CustomersCreate(CreateView):
     model = Customers
     form_class = CustomerForm
     template_name = 'accounting/customer/customerForm.html'
     success_url = reverse_lazy('accounting:customers')

class CustomersEdit(UpdateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'accounting/customer/customerForm.html'
    success_url = reverse_lazy('accounting:customers')

class CustomersDelete(DeleteView):
    model = Customers
    template_name = 'accounting/customer/customers_confirm_delete.html'
    success_url = reverse_lazy('accounting:customers')

class AccountCreate(CreateView):
    model = Accounts
    form_class = AccountForm
    template_name = 'accounting/accounts/accountsForm.html'
    success_url = reverse_lazy('accounting:accounts')

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Accounts.objects.create(name = self.request.POST["name"], description = self.request.POST["description"], accounts_id_id = self.request.POST["accounts_id"], users_id = user.id, primary = None)

class AccountsDescViews(ListView):
    model = AccountDescrip
    template_name = 'accounting/accounts/accountsDescrp.html'


def AccountsViews(requiret):
    primary = Accounts.objects.filter(primary=1)
    lisexp = Accounts.objects.filter(primary=None)
    contexto = {'accounts': lisexp, 'primary': primary}
    return render(requiret, 'accounting/accounts/accountsViews.html', contexto)




