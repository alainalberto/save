from django.contrib import admin

from apps.administration.models import Menus, Business, Profilers, Users, Alerts, Histories, Changerusers, Folders, Files, Calendar, Chat, Directory

# Register your models here.

admin.site.register(Menus)
admin.site.register(Business)
admin.site.register(Profilers)
admin.site.register(Users)
admin.site.register(Alerts)
admin.site.register(Histories)
admin.site.register(Changerusers)
admin.site.register(Folders)
admin.site.register(Files)
admin.site.register(Calendar)
admin.site.register(Chat)
admin.site.register(Directory)
