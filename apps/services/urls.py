from django.conf.urls import *
from django.contrib.auth.decorators import login_required, permission_required
from apps.services.views import *

urlpatterns = [
    #Company
    url(r'^company/$', login_required(permission_required('services.add_company')(CompanyCreate.as_view())), name='company'),

    url(r'^title/$', login_required(permission_required('services.add_title')(CompanyView)), name='title'),
    url(r'^insurance/$', login_required(permission_required('services.add_insurance')(CompanyView)), name='insurance'),
    url(r'^dot/$', login_required(permission_required('services.add_dot')(CompanyView)), name='dot'),
    url(r'^ifta/$', login_required(permission_required('services.add_ifta')(CompanyView)), name='ifta'),
    url(r'^audits/$', login_required(permission_required('services.add_audit')(CompanyView)), name='audits'),
    url(r'^permits/$', login_required(permission_required('services.add_permit')(CompanyView)), name='permits'),
    url(r'^plate/$', login_required(permission_required('services.add_plate')(CompanyView)), name='plate'),
    url(r'^maintenance/$', login_required(permission_required('services.add_maintenance')(CompanyView)), name='maintenance'),
    url(r'^forms/$', login_required(FileView.as_view()), name='forms'),
    url(r'^forms/create$', login_required(FileCreate.as_view()), name='file_create'),
    url(r'^folder/$', login_required(permission_required('tools.add_folder')(CompanyView)), name='folder'),

]