from django.contrib import admin

from apps.services.models import Companies, Contracts, Audit, Drivers, Insurance, Maintenance, Permissions, Trucks, Ifta

# Register your models here.
admin.site.register(Companies)
admin.site.register(Contracts)
admin.site.register(Audit)
admin.site.register(Drivers)
admin.site.register(Insurance)
admin.site.register(Maintenance)
admin.site.register(Permissions)
admin.site.register(Trucks)
admin.site.register(Ifta)
