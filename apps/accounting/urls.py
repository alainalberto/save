from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from apps.accounting.views import *

urlpatterns = [
    url(r'^$', login_required(AccountingPanel.as_view()), name='panel_account'),
    url(r'^accounts/$', login_required(AccountsViews), name='accounts'),
    url(r'^accounts/create/$', login_required(AccountCreate.as_view()), name='account_create'),
    url(r'^accounts/description/$', login_required(AccountsDescViews.as_view()), name='account_descrip'),
    url(r'^customers/$', login_required(CustomersView.as_view()), name='customers'),
    url(r'^customers/create$', login_required(CustomersCreate.as_view()), name='customer_create'),
    url(r'^customers/edit/(?P<pk>\d+)/$', login_required(CustomersEdit.as_view()), name='customer_edit'),
    url(r'^customers/delete/(?P<pk>\d+)/$', login_required(CustomersDelete.as_view()), name='customer_delete'),
    url(r'^customers/service/$', login_required(CustomersService.as_view()), name='customer_service'),
    url(r'^receipts/$', login_required(CustomersView.as_view()), name='receipts'),
    url(r'^payments/$', login_required(CustomersView.as_view()), name='payments'),

    #Employees
    url(r'^employees/$', login_required(EmployeesView.as_view()), name='employees'),
    url(r'^employees/create$', login_required(EmployeesCreate.as_view()), name='employees_create'),
    url(r'^employees/edit/(?P<pk>\d+)/$', login_required(EmployeesEdit.as_view()), name='employees_edit'),
    url(r'^employees/delete/(?P<pk>\d+)/$', login_required(EmployeesDelete.as_view()), name='employees_delete'),

    #Invoices
    url(r'^invoices/$', login_required(InvoicesView.as_view()), name='invoices'),
    url(r'^invoices/create$', login_required(InvoicesCreate.as_view()), name='invoices_create'),
    url(r'^invoices/edit/(?P<pk>\d+)/$', login_required(InvoicesEdit.as_view()), name='invoices_edit'),
    url(r'^invoices/delete/(?P<pk>\d+)/$', login_required(InvoicesDelete.as_view()), name='invoices_delete'),
]