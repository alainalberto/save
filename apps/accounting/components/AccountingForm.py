from django import forms
from apps.accounting.models import Accounts, Customers


class AccountForm(forms.ModelForm):
    class Meta:
        model = Accounts

        fields = [
            'name',
            'description',
            'accounts_id',
        ]
        labels = {
            'name': 'Name',
            'description': 'Description',
            'accounts_id': 'Main Account',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control input-md'}),
            'accounts_id': forms.Select(attrs={'class': 'form-control input-md'}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers

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
