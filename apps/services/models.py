from django.db import models

from  django.contrib.auth.models import User

from apps.administration.models import Folders

from apps.administration.models import Files

from apps.accounting.models import Customers

from apps.accounting.models import Accounts

# Create your models here.


class Companies(models.Model):
    id_com = models.AutoField(primary_key=True)
    folders = models.ForeignKey(Folders, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    customers = models.ForeignKey(Customers, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    attorney = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    fax = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    ein = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    unity = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    deactivate = models.IntegerField(blank=True, null=True)
    deactivate_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Contracts(models.Model):
    id_con = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    files = models.ForeignKey(Files, on_delete=models.CASCADE)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)
    serial = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)


class Audit(models.Model):
    id_aud = models.AutoField(primary_key=True)
    folders = models.ForeignKey(Folders, on_delete=models.CASCADE)  # Field name made lowercase.
    contracts = models.ForeignKey(Contracts, on_delete=models.CASCADE)  # Field name made lowercase.
    companies = models.ForeignKey(Companies, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    type = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    results = models.CharField(max_length=255, blank=True, null=True)

class Drivers(models.Model):
    id_drv = models.AutoField(primary_key=True)
    companies = models.ForeignKey(Companies, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    license_numb = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    lic_date_exp = models.DateField(blank=True, null=True)
    medicard_date_exp = models.DateField(blank=True, null=True)
    drugtest_date = models.DateField(blank=True, null=True)
    drugtest_date_exp = models.DateField(blank=True, null=True)
    mbr_date = models.DateField(blank=True, null=True)
    mbr_date_exp = models.DateField(blank=True, null=True)
    begining_date = models.DateField(blank=True, null=True)
    deactivate = models.IntegerField(blank=True, null=True)
    deactivate_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Insurance(models.Model):
    id_ins = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    accounts = models.ForeignKey(Accounts, on_delete=models.CASCADE)  # Field name made lowercase.
    companies = models.ForeignKey(Companies, on_delete=models.CASCADE)  # Field name made lowercase.
    down_payment = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    pilicy_efective_date = models.DateField(blank=True, null=True)
    pilicy_date_exp = models.DateField(blank=True, null=True)
    liability = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    pilicy_liability = models.CharField(max_length=45, blank=True, null=True)
    cargo = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    cargo_pilicy = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    physical_damage = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    physical_damg_pilicy = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    sale_type = models.CharField(max_length=20, blank=True, null=True)
    sale_date_fee = models.DateField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    comision = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    paid = models.IntegerField(blank=True, null=True)

class Maintenance(models.Model):
    id_mnt = models.AutoField(primary_key=True)
    contracts = models.ForeignKey(Contracts,  on_delete=models.CASCADE)  # Field name made lowercase.
    companies = models.ForeignKey(Companies,  on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    nota = models.CharField(max_length=255, blank=True, null=True)


class Permissions(models.Model):
    id_per = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    companies = models.ForeignKey(Companies, on_delete=models.CASCADE)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    usdot = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    usdot_pin = models.CharField(max_length=20, blank=True, null=True)
    txdmv = models.CharField(max_length=20, blank=True, null=True)
    txdmv_user = models.CharField(max_length=20, blank=True, null=True)
    txdmv_passd = models.CharField(max_length=45, blank=True, null=True)
    txdmv_date = models.DateField(blank=True, null=True)
    txdmv_date_exp = models.DateField(blank=True, null=True)
    mc = models.CharField(max_length=20, blank=True, null=True)
    mc_pin = models.CharField(max_length=20, blank=True, null=True)
    boc3 = models.IntegerField(blank=True, null=True)
    boc3_date = models.DateField(blank=True, null=True)
    ucr = models.IntegerField(blank=True, null=True)
    update = models.DateField(blank=True, null=True)

class Trucks(models.Model):
    id_tru = models.AutoField(primary_key=True)
    companies = models.ForeignKey(Companies, on_delete=models.CASCADE)  # Field name made lowercase.
    type = models.CharField(max_length=45, blank=True, null=True)
    year = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    model = models.CharField(max_length=45, blank=True, null=True)
    serial = models.CharField(max_length=20, blank=True, null=True)
    number = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    insp_date_exp = models.DateField(blank=True, null=True)
    regit_date_exp = models.DateField(blank=True, null=True)
    deactivate = models.IntegerField(blank=True, null=True)
    deactivate_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.number)

class Ifta(models.Model):
    id_ift = models.AutoField(primary_key=True)
    trucks = models.ForeignKey(Trucks, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    customers = models.ForeignKey(Customers, on_delete=models.CASCADE)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    milles = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gallons = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
