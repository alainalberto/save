from django.conf.urls import *

from apps.accounting.views import AccountsViews, AccountingPanel, AccountCreate

urlpatterns = [
    url(r'^$', AccountingPanel.as_view(), name='panel_account'),
    url(r'^accounts/$', AccountsViews, name='accounts'),
    url(r'^accounts/create/$', AccountCreate.as_view(), name='account_create')
]