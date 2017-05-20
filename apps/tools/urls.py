from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from apps.tools.views import *

urlpatterns = [

url(r'^$', login_required(panel_view), name='panel'),
url(r'^calendar/$', login_required(Calendar_Panel), name='calendar'),
url(r'^calendar/create$', login_required(PostCalendar.as_view()), name='calendar_create'),
url(r'^password/$', login_required(panel_view), name='password'),
url(r'^document/$', login_required(panel_view), name='document'),

]
