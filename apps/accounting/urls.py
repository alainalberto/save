from django.conf.urls import url, include

from apps.accounting.views import AccountsViews, AccountingPanel

urlpatterns = [
    url(r'^$', AccountingPanel.as_view(), name='panel_account'),
    url(r'^accounts/', AccountsViews, name='accounts')


]