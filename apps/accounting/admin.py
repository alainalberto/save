from django.contrib import admin

from apps.accounting.models import Accounts, Customers, Invoices, Employees, Fee, Items, Receipts, Salary, AccountDescrip, InvoicesHasItems

# Register your models here.

admin.site.register(Accounts)
admin.site.register(Customers)
admin.site.register(Employees)
admin.site.register(Invoices)
admin.site.register(Items)
admin.site.register(Receipts)
admin.site.register(Salary)
admin.site.register(Fee)
admin.site.register(AccountDescrip)
admin.site.register(InvoicesHasItems)
