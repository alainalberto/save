from django.conf.urls import *
from django.contrib.auth.decorators import login_required, permission_required
from apps.services.views import *

urlpatterns = [

    url(r'^company/$', login_required(permission_required('services.add_company')(CompanyView.as_view())), name='company'),
    url(r'^title/$', login_required(permission_required('services.add_title')(CompanyView.as_view())), name='title'),
    url(r'^insurance/$', login_required(permission_required('services.add_insurance')(CompanyView.as_view())), name='insurance'),
    url(r'^dot/$', login_required(permission_required('services.add_dot')(CompanyView.as_view())), name='dot'),
    url(r'^ifta/$', login_required(permission_required('services.add_ifta')(CompanyView.as_view())), name='ifta'),
    url(r'^audits/$', login_required(permission_required('services.add_audit')(CompanyView.as_view())), name='audits'),
    url(r'^permits/$', login_required(permission_required('services.add_permit')(CompanyView.as_view())), name='permits'),
    url(r'^plate/$', login_required(permission_required('services.add_plate')(CompanyView.as_view())), name='plate'),
    url(r'^maintenance/$', login_required(permission_required('services.add_maintenance')(CompanyView.as_view())), name='maintenance'),
    url(r'^forms/$', login_required(), name='forms'),
    url(r'^folder/$', login_required(permission_required('tools.add_folder')(CompanyView.as_view())), name='folder'),

]