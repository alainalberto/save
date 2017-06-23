from django.conf.urls import *
from django.contrib.auth.decorators import login_required, permission_required
from apps.logistic.components.LogisticPDF import *
from apps.logistic.views import *

urlpatterns = [

    # Load
    url(r'^loads/$', login_required(permission_required('logistic.add_load')(LoadsView.as_view())), name='loads'),
    url(r'^loads/create$', login_required(permission_required('logistic.add_load')(LoadsCreate.as_view())), name='load_create'),
    url(r'^loads/edit/(?P<pk>\d+)/$', login_required(permission_required('logistic.change_load')(LoadsEdit.as_view())), name='load_edit'),
    url(r'^loads/(?P<pk>\d+)/$', login_required(permission_required('logistic.delete_load')(LoadsDelete.as_view())), name='load_delete'),
    url(r'^loads/print/(?P<pk>\d+)/$', login_required(permission_required('logistic.add_load')(LoadPDF)), name='load_pdf'),


    url(r'^drivers/$', login_required(permission_required('logistic.add_driverslogt')(DriversView.as_view())), name='drivers'),
    url(r'^drivers/create$', login_required(permission_required('logistic.add_driverslogt')(DriversCreate.as_view())), name='drivers_create'),
    url(r'^drivers/edit/(?P<pk>\d+)/$', login_required(permission_required('logistic.change_driverslogt')(DriversEdit.as_view())), name='drivers_edit'),
    url(r'^drivers/(?P<pk>\d+)/$', login_required(permission_required('logistic.delete_driverslogt')(DriversDelete.as_view())), name='drivers_delete'),

    url(r'^dispatch/$', login_required(permission_required('logistic.add_dispatchlogt')(DispatchView.as_view())), name='dispatch'),
    url(r'^dispatch/create$', login_required(permission_required('logistic.add_dispatchlogt')(DispatchCreate.as_view())), name='dispatch_create'),
    url(r'^dispatch/edit/(?P<pk>\d+)/$', login_required(permission_required('logistic.change_dispatchlogt')(DispatchEdit.as_view())), name='dispatch_edit'),
    url(r'^dispatch/(?P<pk>\d+)/$', login_required(permission_required('logistic.delete_dispatchlogt')(DispatchDelete.as_view())), name='dispatch_delete'),


    url(r'^trucks/$', login_required(), name='trucks'),
    url(r'^travel/$', login_required(), name='travel'),
    url(r'^infcompany/$', login_required(), name='infcompany'),
]