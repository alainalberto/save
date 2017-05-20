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


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Customer

        fields = [
            'name',
            'lastname',
            'no_social',
            'address',
            'phone',
            'email',
            'business',
            'folders',
            'users',
        ]
        labels = {
            'name' : 'Name',
            'lastname' : 'Last Name',
            'no_social' : 'SSN',
            'address' : 'Address',
            'phone' : 'Phone',
            'email' : 'Email',
            'business' : 'Busines',
            'folders' : 'Folders',
            'users' : 'User',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control input-md'}),
            'no_social': forms.NumberInput(attrs={'placeholder': 'SSN', 'class': 'form-control input-md'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Telepone Number', 'class': 'form-control input-md'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control input-md'}),
            'business': forms.Select(attrs={'class': 'form-control input-md'}),
            'folders': forms.Select(attrs={'class': 'form-control input-md'}),
            'users': forms.Select(attrs={'class': 'form-control input-md'}),
        }
