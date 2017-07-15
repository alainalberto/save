from django.conf.urls import *
from django.contrib.auth.decorators import login_required, permission_required
from apps.services.views import *

urlpatterns = [
    #Company
    url(r'^company/create$', login_required(permission_required('services.add_companie')(CompanyCreate.as_view())), name='company_create'),
    url(r'^company/create/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_companie')(CompanyCreate.as_view())), name='company_create_popup'),
    url(r'^company/edit/(?P<pk>\d+)/$', login_required(permission_required('services.change_companie')(CompanyEdit.as_view())), name='company_edit'),
    url(r'^company/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.change_companie')(CompanyEdit.as_view())), name='company_edit_popup'),

    #Forms
    url(r'^forms/$', login_required(FileView.as_view()), name='forms'),
    url(r'^forms/create$', login_required(permission_required('tools.add_file')(FileCreate.as_view())), name='file_create'),
    url(r'^forms/edit/(?P<pk>\d+)/$', login_required(permission_required('tools.change_file')(FileEdit.as_view())), name='file_edit'),
    url(r'^forms/(?P<pk>\d+)/$', login_required(permission_required('tools.delete_file')(FileDelete.as_view())), name='file_delete'),

    #Folder
    url(r'^folder/$', login_required(permission_required('tools.add_file')(FolderView.as_view())), name='folder'),
    url(r'^folder/create$', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create'),
    url(r'^folder/create/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create_popup'),
    url(r'^folder/edit/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderEdit.as_view())), name='folder_edit'),
    url(r'^folder/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('tools.add_file')(FolderEdit.as_view())), name='folder_edit_popup'),
    url(r'^folder/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderDelete.as_view())), name='folder_delete'),
    url(r'^folder/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('tools.add_file')(FolderDelete.as_view())), name='folder_delete_popup'),


    url(r'^title/$', login_required(permission_required('services.add_title')(CompanyView)), name='title'),
    url(r'^insurance/$', login_required(permission_required('services.add_insurance')(CompanyView)), name='insurance'),
    url(r'^dot/$', login_required(permission_required('services.add_dot')(CompanyView)), name='dot'),
    url(r'^ifta/$', login_required(permission_required('services.add_ifta')(CompanyView)), name='ifta'),
    url(r'^audits/$', login_required(permission_required('services.add_audit')(CompanyView)), name='audits'),
    url(r'^permits/$', login_required(permission_required('services.add_permit')(CompanyView)), name='permits'),
    url(r'^plate/$', login_required(permission_required('services.add_plate')(CompanyView)), name='plate'),
    url(r'^maintenance/$', login_required(permission_required('services.add_maintenance')(CompanyView)), name='maintenance'),

]