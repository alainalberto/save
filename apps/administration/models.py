from django.db import models

# Create your models here.

# Model Table menus
class Menus(models.Model):
    id_men = models.AutoField(primary_key=True)
    menus_id = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

# Model Table business
class Business(models.Model):
    id_bus = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=255)
    phone = models.DecimalField(max_digits=10, decimal_places=0)
    fax = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    logo = models.CharField(max_length=255)
    date_created = models.DateField()
    active = models.IntegerField()
    date_deactivated = models.DateField(blank=True, null=True)
    messager = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

# Model Table profilers
class Profilers(models.Model):
    id_prf = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField()
    date_deactivated = models.DateField(blank=True, null=True)
    menus = models.ManyToManyField(Menus, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

# Model Table users
class Users(models.Model):
    id_use = models.AutoField(primary_key=True)
    profilers = models.ForeignKey(Profilers, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=20)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    active = models.IntegerField()
    date_deactivated = models.DateTimeField(blank=True, null=True)
    online = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)



# Model Tables relation profiler-alerts
class Alerts(models.Model):
    id_alt = models.AutoField(primary_key=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)  # Field name made lowercase.
    category = models.CharField(max_length=20)
    drescription = models.CharField(max_length=255)
    create_date = models.DateField(auto_now_add=True)
    show_date = models.DateField()
    end_date = models.DateField()
    active = models.IntegerField()
    profilers = models.ManyToManyField(Profilers, blank=True)

    def __str__(self):
        return '{}'.format(self.drescription)

# Model Table histories
class Histories(models.Model):
    id_hst = models.AutoField(primary_key=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)  # Field name made lowercase.
    date= models.DateTimeField(auto_now_add=True)
    acction = models.CharField(max_length=20)

# Model Table histories
class Changerusers(models.Model):
    id_chg = models.AutoField(primary_key=True)
    histories = models.ForeignKey(Histories, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    value_before = models.CharField(max_length=350, blank=True, null=True)
    value_after = models.CharField(max_length=350, blank=True, null=True)

# Model Table folders
class Folders(models.Model):
    id_fld = models.AutoField(primary_key=True)
    folders_id = models.ForeignKey('self', on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

# Model Table files
class Files(models.Model):
    id_fil = models.AutoField(primary_key=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)  # Field name made lowercase.
    folders = models.ForeignKey(Folders, on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    drescription = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    date_save = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Calendar(models.Model):
    id_cld = models.AutoField(primary_key=True)
    users = models.ForeignKey('Users', on_delete=models.CASCADE)  # Field name made lowercase.
    title = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.title)

class Chat(models.Model):
    id_cht = models.AutoField(primary_key=True)
    users = models.ForeignKey('Users', on_delete=models.CASCADE)  # Field name made lowercase.
    date = models.DateTimeField(auto_now_add=True)
    messager = models.CharField(max_length=255)


class Directory(models.Model):
    id_dir = models.AutoField(primary_key=True)
    users = models.ForeignKey('Users', on_delete=models.CASCADE)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)
