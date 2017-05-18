from django.db import models

from  django.contrib.auth.models import User

from apps.tools.models import Folder

from apps.tools.models import File

from apps.accounting.models import Customer

from apps.accounting.models import Account

# Create your models here.


class Companie(models.Model):
    id_com = models.AutoField(primary_key=True)
    folders = models.ForeignKey(Folder, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    attorney = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    fax = models.IntegerField(blank=True, null=True)
    ein = models.IntegerField(blank=True, null=True)
    logo = models.ImageField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    unity = models.IntegerField(blank=True, null=True)
    deactivate = models.BooleanField(default=False)
    deactivate_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Contract(models.Model):
    id_con = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    files = models.ForeignKey(File, on_delete=models.CASCADE)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)
    serial = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)


class Audit(models.Model):
    id_aud = models.AutoField(primary_key=True)
    folders = models.ForeignKey(Folder, on_delete=models.CASCADE)  # Field name made lowercase.
    contracts = models.ForeignKey(Contract, on_delete=models.CASCADE)  # Field name made lowercase.
    companies = models.ForeignKey(Companie, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    type = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    results = models.CharField(max_length=255, blank=True, null=True)

class Driver(models.Model):
    id_drv = models.AutoField(primary_key=True)
    companies = models.ForeignKey(Companie, on_delete=models.CASCADE)  # Field name made lowercase.
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
    deactivate = models.BooleanField(default=False)
    deactivate_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Insurance(models.Model):
    id_ins = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE)  # Field name made lowercase.
    companies = models.ForeignKey(Companie, on_delete=models.CASCADE)  # Field name made lowercase.
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
    paid = models.BooleanField(default=False)

class Maintenance(models.Model):
    id_mnt = models.AutoField(primary_key=True)
    contracts = models.ForeignKey(Contract,  on_delete=models.CASCADE)  # Field name made lowercase.
    companies = models.ForeignKey(Companie,  on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    nota = models.CharField(max_length=255, blank=True, null=True)


class Permission(models.Model):
    id_per = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    companies = models.ForeignKey(Companie, on_delete=models.CASCADE)  # Field name made lowercase.
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
    companies = models.ForeignKey(Companie, on_delete=models.CASCADE)  # Field name made lowercase.
    type = models.CharField(max_length=45, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=45, blank=True, null=True)
    serial = models.CharField(max_length=20, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    insp_date_exp = models.DateField(blank=True, null=True)
    regit_date_exp = models.DateField(blank=True, null=True)
    deactivate = models.BooleanField(default=False)
    deactivate_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.number)

class Ifta(models.Model):
    id_ift = models.AutoField(primary_key=True)
    trucks = models.ForeignKey(Trucks, on_delete=models.CASCADE)  # Field name made lowercase.
    users = models.ForeignKey(User, on_delete=models.CASCADE)  # Field name made lowercase.
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    milles = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    gallons = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
