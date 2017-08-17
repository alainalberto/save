from django.conf.urls import *
from django.contrib.auth.decorators import login_required, permission_required
from apps.services.views import *

urlpatterns = [
    #Company
    url(r'^company/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_companie')(CompanyView)), name='company'),
    url(r'^company/create$', login_required(permission_required('services.add_companie')(CompanyCreate.as_view())), name='company_create'),
    url(r'^company/create/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_companie')(CompanyCreate.as_view())), name='company_create_popup'),
    url(r'^company/edit/(?P<pk>\d+)/$', login_required(permission_required('services.change_companie')(CompanyEdit.as_view())), name='company_edit'),
    url(r'^company/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.change_companie')(CompanyEdit.as_view())), name='company_edit_popup'),
    url(r'^company/(?P<pk>\d+)/$', login_required(permission_required('services.delete_companie')(CompanyDelete.as_view())), name='company_delete'),

    #Forms
    url(r'^forms/$', login_required(FormView.as_view()), name='forms'),
    url(r'^forms/create$', login_required(permission_required('tools.add_file')(FormCreate.as_view())), name='file_create'),
    url(r'^forms/edit/(?P<pk>\d+)/$', login_required(permission_required('tools.change_file')(FormEdit.as_view())), name='file_edit'),
    url(r'^forms/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('tools.change_file')(FormEdit.as_view())), name='file_edit_popup'),
    url(r'^forms/(?P<pk>\d+)/$', login_required(permission_required('tools.delete_file')(FormDelete.as_view())), name='file_delete'),

    #Folder
    url(r'^folder/$', login_required(permission_required('tools.add_file')(FolderView.as_view())), name='folder'),
    url(r'^folder/create$', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create'),
    url(r'^folder/create/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create_popup'),
    url(r'^folder/edit/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderEdit.as_view())), name='folder_edit'),
    url(r'^folder/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('tools.add_file')(FolderEdit.as_view())), name='folder_edit_popup'),
    url(r'^folder/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderDelete.as_view())), name='folder_delete'),

    #IFTA
    url(r'^ifta/$', login_required(permission_required('services.add_ifta')(CompanyView)), name='ifta'),
    url(r'^ifta/create$', login_required(permission_required('services.add_ifta')(CompanyView)), name='ifta_create'),

    #Permit
    url(r'^permits/$', login_required(permission_required('services.add_permission')(PermitView)), name='permits'),
    url(r'^permit/create$', login_required(permission_required('services.add_permission')(PermitCreate.as_view())), name='permit_create'),
    url(r'^permit/create/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_permission')(PermitCreate.as_view())), name='permit_create_popup'),
    url(r'^permit/edit/(?P<pk>\d+)/$', login_required(permission_required('services.change_permission')(PermitEdit.as_view())), name='permit_edit'),
    url(r'^permit/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.change_permission')(CompanyEdit.as_view())), name='permit_edit_popup'),
    url(r'^permit/(?P<pk>\d+)/$', login_required(permission_required('services.delete_permission')(PermitDelete.as_view())), name='permit_delete'),

    #Mtt
    url(r'^maintenance/$', login_required(permission_required('services.add_maintenance')(MttCreate.as_view())), name='maintenance'),

    url(r'^title/$', login_required(permission_required('services.add_title')(CompanyView)), name='title'),
    url(r'^insurance/$', login_required(permission_required('services.add_insurance')(CompanyView)), name='insurance'),
    url(r'^dot/$', login_required(permission_required('services.add_dot')(CompanyView)), name='dot'),
    url(r'^audits/$', login_required(permission_required('services.add_audit')(CompanyView)), name='audits'),
    url(r'^plate/$', login_required(permission_required('services.add_plate')(CompanyView)), name='plate'),


]