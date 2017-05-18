from django.contrib import admin

from apps.logistic.models import *

# Register your models here.
admin.site.register(Load)
admin.site.register(TrucksLogt)
admin.site.register(DriversLogt)
admin.site.register(PermissionsLogt)
admin.site.register(InsuranceLogt)
admin.site.register(IftaLogt)
admin.site.register(TravelExpense)
admin.site.register(LoadsHasFee)
admin.site.register(InvoicesHasLoad)
