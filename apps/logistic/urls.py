from django.conf.urls import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^loads/$', login_required(), name='loads'),
    url(r'^drives/$', login_required(), name='drives'),
    url(r'^trucks/$', login_required(), name='trucks'),
    url(r'^travel/$', login_required(), name='travel'),
    url(r'^infcompany/$', login_required(), name='infcompany'),
]