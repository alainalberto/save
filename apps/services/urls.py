from django.conf.urls import *
from django.contrib.auth.decorators import login_required, permission_required
from apps.services.views import *

urlpatterns = [
    #Company
    url(r'^permit/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_permit')(PermitView)), name='permit'),
    url(r'^permit/create$', login_required(permission_required('services.add_permit')(PermitCreate.as_view())), name='permit_create'),
    url(r'^permit/create/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.add_permit')(PermitCreate.as_view())), name='permit_create_popup'),
    url(r'^permit/edit/(?P<pk>\d+)/$', login_required(permission_required('services.change_permit')(PermitEdit.as_view())), name='permit_edit'),
    url(r'^permit/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('services.change_permit')(PermitEdit.as_view())), name='permit_edit_popup'),
    url(r'^permit/(?P<pk>\d+)/$', login_required(permission_required('services.delete_permit')(PermitDelete.as_view())), name='permit_delete'),

    #Forms
    url(r'^forms/$', login_required(FormView.as_view()), name='forms'),
    url(r'^forms/create$', login_required(permission_required('tools.add_file')(FormCreate.as_view())), name='file_create'),
    url(r'^forms/edit/(?P<pk>\d+)/$', login_required(permission_required('tools.change_file')(FormEdit.as_view())), name='file_edit'),
    url(r'^forms/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$', login_required(permission_required('tools.change_file')(FormEdit.as_view())), name='file_edit_popup'),
    url(r'^forms/(?P<pk>\d+)/$', login_required(permission_required('tools.delete_file')(FormDelete.as_view())), name='file_delete'),

    #Folder
    url(r'^folder/$', login_required(permission_required('tools.add_file')(FolderView.as_view())), name='folder'),
    url(r'^folder/create$', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create'),
    url(r'^folder/create/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderCreate.as_view())), name='folder_create_popup'),
    url(r'^folder/edit/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderEdit.as_view())), name='folder_edit'),
    url(r'^folder/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',login_required(permission_required('tools.add_file')(FolderEdit.as_view())), name='folder_edit_popup'),
    url(r'^folder/(?P<pk>\d+)/$', login_required(permission_required('tools.add_file')(FolderDelete.as_view())), name='folder_delete'),

    #IFTA
    url(r'^ifta/$', login_required(permission_required('services.add_ifta')(PermitView)), name='ifta'),
    url(r'^ifta/create$', login_required(permission_required('services.add_ifta')(PermitView)), name='ifta_create'),


    #Equipment
    url(r'^equipment/view/(?P<pk>\d+)&(?P<popup>[^/]+)/$',
        login_required(permission_required('services.add_equipment')(EquipmentView)), name='equipment'),
    url(r'^permit/create$', login_required(permission_required('services.add_equipment')(EquipmentCreate.as_view())),
        name='equipment_create'),
    url(r'^equipment/create/(?P<pk>\d+)&(?P<popup>[^/]+)/$',
        login_required(permission_required('services.add_equipment')(EquipmentCreate.as_view())), name='equipment_create_popup'),
    url(r'^equipment/edit/(?P<pk>\d+)/$',
        login_required(permission_required('services.change_equipment')(EquipmentEdit.as_view())), name='equipment_edit'),
    url(r'^equipment/edit/(?P<pk>\d+)&(?P<popup>[^/]+)/$',
        login_required(permission_required('services.change_equipment')(EquipmentEdit.as_view())), name='equipment_edit_popup'),
    url(r'^equipment/(?P<pk>\d+)/$', login_required(permission_required('services.delete_equipment')(EquipmentDelete.as_view())),
        name='equipment_delete'),
    #Insurance
    url(r'^insurance/$', login_required(permission_required('services.add_insurance')(PermitView)), name='insurance'),

    url(r'^audits/$', login_required(permission_required('services.add_audit')(PermitView)), name='audits'),


]