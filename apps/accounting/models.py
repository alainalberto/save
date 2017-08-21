from django.db import models

from django.contrib.auth.models import User

from apps.tools.models import Folder, Busines, File

from datetime import datetime



# Create your models here.

# Model Table accounts
class Account(models.Model):
    id_acn = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE) # Field name made lowercase.
    business = models.ForeignKey(Busines, on_delete=models.CASCADE)
    accounts_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True, null=True)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.name)


class Customer(models.Model):
    id_cut = models.AutoField(primary_key=True)
    business = models.ForeignKey(Busines, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User,  on_delete=models.CASCADE)  # Field name made lowercase.
    folders = models.ForeignKey(Folder,  on_delete=models.CASCADE)  # Field name made lowercase.
    fullname = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    no_social = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255)
    deactivated = models.BooleanField(default=False)
    date_deactivated = models.DateField(blank=True, null=True)
    usdot = models.CharField(max_length=20,blank=True, null=True)
    mc = models.CharField(max_length=20,blank=True, null=True)
    txdmv = models.CharField(max_length=20,blank=True, null=True)
    ein = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.fullname)

class Employee(models.Model):
    id_emp = models.AutoField(primary_key=True)
    business = models.ForeignKey(Busines,  on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    social_no = models.CharField(max_length=20, blank=True, null=True)
    date_admis = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    type_salary = models.CharField(max_length=20, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)
    deactivated = models.BooleanField(default=False)
    date_deactivated = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Invoice(models.Model):
    id_inv = models.AutoField(primary_key=True)
    customers = models.ForeignKey(Customer,  on_delete=models.CASCADE)  # Field name made lowercase.
    business = models.ForeignKey(Busines,  on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User,  on_delete=models.CASCADE)  # Field name made lowercase.
    serial = models.IntegerField()
    type = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    waytopay = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=True)
    prefix = models.CharField(max_length=4, default='inv')
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.serial)


class Item(models.Model):
    id_ite = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Receipt(models.Model):
    id_rec = models.AutoField(primary_key=True)
    accounts = models.ForeignKey(Account,  on_delete=models.CASCADE)  # Field name made lowercase.
    business = models.ForeignKey(Busines,  on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    files = models.ForeignKey(File, on_delete=models.CASCADE)
    serial = models.CharField(max_length=20)
    start_date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"))
    end_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=45)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    waytopay = models.CharField(max_length=20)
    paid = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.serial)

class Payment(models.Model):
    id_sal = models.AutoField(primary_key=True)
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    business = models.ForeignKey(Busines, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    serial = models.CharField(max_length=20, blank=True, null=True)
    discount  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    value  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    waytopay = models.CharField(max_length=20)

    def __str__(self):
        return '{}'.format(self.name)

class Fee(models.Model):
    id_fee = models.AutoField(primary_key=True)
    accounts = models.ForeignKey(Account,  on_delete=models.CASCADE)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.description)

class InvoicesHasItem(models.Model):
    id_ind = models.AutoField(primary_key=True)
    invoices = models.ForeignKey(Invoice, on_delete=models.CASCADE)  # Field name made lowercase.
    items = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)  # Field name made lowercase.
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    quantity = models.IntegerField()
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.description)

class AccountDescrip(models.Model):
    id_acd = models.AutoField(primary_key=True)
    users = models.ForeignKey(User,  on_delete=models.CASCADE)  # Field name made lowercase.
    accounts = models.ForeignKey(Account,  on_delete=models.CASCADE)  # Field name made lowercase.
    type = models.CharField(max_length=20, blank=True, null=True)
    document = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    waytopay = models.CharField(max_length=20, blank=True, null=True)

    def get_document(self):
        if self.type == "Receipt":
            return Receipt.objects.get(id_rec=self.document)
        if self.type == "Item":
            return Item.objects.get(id_itm=self.document)
        if self.type == "Payment":
            return Payment.objects.get(id_sal=self.document)

class EmployeeHasPayment(models.Model):
    id_pym = models.AutoField(primary_key=True)
    payments = models.ForeignKey(Payment, on_delete=models.CASCADE)  # Field name made lowercase.
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Field name made lowercase.

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)
    users = models.ForeignKey(User,  on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=300, blank=True, null=True)

