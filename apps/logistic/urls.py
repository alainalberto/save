from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from apps.logistic.views import *

urlpatterns = [

    # Load
    url(r'^loads/$', login_required(LoadsView.as_view()), name='loads'),
    url(r'^loads/create$', login_required(LoadsCreate.as_view()), name='load_create'),
    url(r'^loads/edit/(?P<pk>\d+)/$', login_required(LoadsEdit.as_view()), name='load_edit'),
    url(r'^loads/(?P<pk>\d+)/$', login_required(LoadsDelete.as_view()), name='load_delete'),
    url(r'^loads/print/(?P<pk>\d+)/$', login_required(LoadPDF.as_view()), name='load_pdf'),


    url(r'^drivers/$', login_required(DriversView.as_view()), name='drivers'),
    url(r'^drivers/create$', login_required(DriversCreate.as_view()), name='drivers_create'),
    url(r'^drivers/edit/(?P<pk>\d+)/$', login_required(DriversEdit.as_view()), name='drivers_edit'),
    url(r'^drivers/(?P<pk>\d+)/$', login_required(DriversDelete.as_view()), name='drivers_delete'),

    url(r'^dispatch/$', login_required(DispatchView.as_view()), name='dispatch'),
    url(r'^dispatch/create$', login_required(DispatchCreate.as_view()), name='dispatch_create'),
    url(r'^dispatch/edit/(?P<pk>\d+)/$', login_required(DispatchEdit.as_view()), name='dispatch_edit'),
    url(r'^dispatch/(?P<pk>\d+)/$', login_required(DispatchDelete.as_view()), name='dispatch_delete'),


    url(r'^trucks/$', login_required(), name='trucks'),
    url(r'^travel/$', login_required(), name='travel'),
    url(r'^infcompany/$', login_required(), name='infcompany'),
]