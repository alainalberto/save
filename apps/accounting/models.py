from django.db import models

from  django.contrib.auth.models import User

from apps.tools.models import Folders

from apps.tools.models import Business


# Create your models here.

# Model Table accounts
class Accounts(models.Model):
    id_acn = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    accounts_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True, null=True)
    primary = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Customers(models.Model):
    id_cut = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User,  on_delete=models.CASCADE)  # Field name made lowercase.
    folders = models.ForeignKey(Folders,  on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    no_social = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Employees(models.Model):
    id_emp = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business,  on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    adress = models.CharField(max_length=255, blank=True, null=True)
    social_no = models.CharField(max_length=20, blank=True, null=True)
    date_admis = models.DateField(blank=True, null=True)
    phone = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    type_salary = models.CharField(max_length=20, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Invoices(models.Model):
    id_inv = models.AutoField(primary_key=True)
    accounts = models.ForeignKey(Accounts,  on_delete=models.CASCADE)  # Field name made lowercase.
    customers = models.ForeignKey(Customers,  on_delete=models.CASCADE)  # Field name made lowercase.
    business = models.ForeignKey(Business,  on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User,  on_delete=models.CASCADE)  # Field name made lowercase.
    serial = models.IntegerField()
    date_start = models.DateField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    start_date = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    waytopay = models.CharField(max_length=20, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    paid = models.IntegerField(blank=True, null=True)
    prefix = models.CharField(max_length=4, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.serial)


class Items(models.Model):
    id_ite = models.AutoField(primary_key=True)
    accounts = models.ForeignKey(Accounts,  on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Receipts(models.Model):
    id_rec = models.AutoField(primary_key=True)
    accounts = models.ForeignKey(Accounts,  on_delete=models.CASCADE)  # Field name made lowercase.
    business = models.ForeignKey(Business,  on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    serial = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=45)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    weytopay = models.CharField(max_length=20)
    paid = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.name)

class Salary(models.Model):
    id_sal = models.AutoField(primary_key=True)
    accounts = models.ForeignKey(Accounts, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    employees = models.ForeignKey(Employees,  on_delete=models.CASCADE)  # Field name made lowercase.
    start_date_sal = models.DateField(blank=True, null=True)
    end_date_sal = models.DateField(blank=True, null=True)
    serial_sal = models.CharField(max_length=20, blank=True, null=True)
    discount_sal = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    value_sal = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Fee(models.Model):
    id_fee = models.AutoField(primary_key=True)
    accounts = models.ForeignKey(Accounts,  on_delete=models.CASCADE)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.description)

class AccountDescrip(models.Model):
    id_acd = models.AutoField(primary_key=True)
    users = models.ForeignKey(User,  on_delete=models.CASCADE)  # Field name made lowercase.
    accounts = models.ForeignKey(Accounts,  on_delete=models.CASCADE)  # Field name made lowercase.
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.TextField()  # This field type is a guess.


class InvoicesHasItems(models.Model):
    id_ind = models.AutoField(primary_key=True)
    invoices = models.ForeignKey(Invoices, on_delete=models.CASCADE)  # Field name made lowercase.
    items = models.ForeignKey(Items, on_delete=models.CASCADE)  # Field name made lowercase.
    quantity_ind = models.IntegerField(blank=True, null=True)
    value_ind = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
