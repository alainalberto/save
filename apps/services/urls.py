from django.conf.urls import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^company/$', login_required(), name='company'),
    url(r'^title/$', login_required(), name='title'),
    url(r'^insurance/$', login_required(), name='insurance'),
    url(r'^dot/$', login_required(), name='dot'),
    url(r'^ifta/$', login_required(), name='ifta'),
    url(r'^audits/$', login_required(), name='audits'),
    url(r'^permits/$', login_required(), name='permits'),
    url(r'^plate/$', login_required(), name='plate'),
    url(r'^maintenance/$', login_required(), name='maintenance'),

]