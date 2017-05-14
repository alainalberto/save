from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from FirstCall.views import panel_view

urlpatterns = [

url(r'^$', login_required(panel_view), name='panel'),
url(r'^calendar/$', login_required(panel_view), name='calendar'),
url(r'^password/$', login_required(panel_view), name='password'),
url(r'^document/$', login_required(panel_view), name='document'),

]
