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


    url(r'^drives/$', login_required(), name='drives'),
    url(r'^dispatch/$', login_required(), name='dispatch'),
    url(r'^trucks/$', login_required(), name='trucks'),
    url(r'^travel/$', login_required(), name='travel'),
    url(r'^infcompany/$', login_required(), name='infcompany'),
]