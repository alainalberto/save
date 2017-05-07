from django.contrib import admin

from apps.logistic.models import Loads, TrucksLogt, DriversLogt, PermissionsLogt, InsuranceLogt, IftaLogt, TravelExpenses, LoadsHasFee, InvoicesHasLoads

# Register your models here.
admin.site.register(Loads)
admin.site.register(TrucksLogt)
admin.site.register(DriversLogt)
admin.site.register(PermissionsLogt)
admin.site.register(InsuranceLogt)
admin.site.register(IftaLogt)
admin.site.register(TravelExpenses)
admin.site.register(LoadsHasFee)
admin.site.register(InvoicesHasLoads)
