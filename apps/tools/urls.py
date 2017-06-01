from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from apps.tools.views import *

urlpatterns = [

url(r'^$', login_required(panel_view), name='panel'),
url(r'^calendar/$', login_required(Calendar_Panel), name='calendar'),
url(r'^calendar/create$', login_required(PostCalendar.as_view()), name='calendar_create'),
url(r'^password/$', login_required(panel_view), name='password'),
url(r'^document/$', login_required(panel_view), name='document'),
url(r'^notification/$', login_required(NotificationView), name='notification'),
url(r'^alert/$', login_required(AlertView), name='alert'),
url(r'^urgent/$', login_required(UrgentView), name='urgent'),
url(r'^alerts/create$', login_required(AlertsCreate.as_view()), name='alert_create'),
url(r'^alerts/edit/(?P<pk>\d+)/$', login_required(AlertstEdit.as_view()), name='alert_edit'),
url(r'^alerts/delete/(?P<pk>\d+)/$', login_required(AlertsDelete.as_view()), name='alert_delete'),

]