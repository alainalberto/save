from django import forms
from apps.services.models import *


class CompanyForm(forms.Form):
    name = forms.CharField(label='Name:'),
    attorney = forms.CharField(label='Attoney:'),
    address = forms.CharField(label='Address:'),
    phone = forms.IntegerField(label='Phone:'),
    fax = forms.IntegerField(label='Fax:'),
    ein = forms.IntegerField(label='EIN:'),
    logo = forms.FileField(label='Logo:'),
    unity = forms.IntegerField(label='Unity:'),
    deactivate = forms.BooleanField(label='Deactivated:'),


