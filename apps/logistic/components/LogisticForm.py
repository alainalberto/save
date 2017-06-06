from django import forms
from apps.logistic.models import *



class LoadsForm(forms.ModelForm):
    class Meta:
        model = Load

        fields = [
            'broker',
            'pickup_from',
            'pickup_date',
            'deliver',
            'dispatch',
            'driver',
            'value',
            'number',
            'paid',
            'note',
        ]
        labels = {
            'broker': 'Broker Name:',
            'pickup_from': 'Pick up From:',
            'pickup_date': 'Pick up Date:',
            'deliver': 'Deliver to:',
            'dispatch': 'Dispatch:',
            'driver': 'Driver:',
            'value': 'Agreed Amount:',
            'number': 'Load Number:',
            'paid': 'Paid:',
            'note': 'Note:',
        }
        widgets = {
            'broker': forms.TextInput(attrs={'placeholder': 'Broker', 'class': 'form-control input-md'}),
            'pickup_from': forms.TextInput(attrs={'placeholder': 'Pick up From', 'class': 'form-control input-md'}),
            'pickup_date': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'deliver': forms.TextInput(attrs={'placeholder': 'Deliver to', 'class': 'form-control input-md'}),
            'dispatch': forms.Select(attrs={'class': 'form-control input-md'}),
            'driver': forms.Select(attrs={'class': 'form-control input-md'}),
            'value': forms.NumberInput(attrs={'placeholder': 'Value', 'class': 'form-control input-md'}),
            'number': forms.TextInput(attrs={'placeholder': 'Number', 'class': 'form-control input-md'}),
            'paid': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'Note': forms.Textarea(attrs={'class': 'form-control input-md'}),

        }


class DriversForm(forms.ModelForm):
    class Meta:
        model = DriversLogt

        fields = [
            'name',
            'comercial_name',
            'license_numb',
            'address',
            'dob',
            'lic_date_exp',
            'medicard_date_exp',
            'drugtest_date',
            'drugtest_date_exp',
            'mbr_date',
            'mbr_date_exp',
            'begining_date',
            'deactivate',
            'date_deactivated',
        ]
        labels = {
            'name': 'Name:',
            'comercial_name': 'Commercial Name:',
            'license_numb': 'License Number:',
            'address': 'Address:',
            'dob': 'Dob:',
            'lic_date_exp': 'Lic Date Exp:',
            'medicard_date_exp': 'Medicard Date Exp:',
            'drugtest_date': 'Drugtest Date:',
            'drugtest_date_exp': 'Drugtest Date Exp:',
            'mbr_date': 'Mbr Date:',
            'mbr_date_exp': 'Mbr Date Exp:',
            'begining_date': 'Beginning Date:',
            'deactivate': 'Deactivate:',
            'date_deactivated': 'Deactivated Date:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md'}),
            'comercial_name': forms.TextInput(attrs={'placeholder': 'Commercial Name', 'class': 'form-control input-md'}),
            'license_numb': forms.NumberInput(attrs={'placeholder': 'License Number', 'class': 'form-control input-md'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md'}),
            'dob': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'lic_date_exp': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'medicard_date_exp': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'drugtest_date': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'drugtest_date_exp': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'mbr_date': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'mbr_date_exp': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'begining_date': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'deactivate': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'date_deactivated': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),

        }


class DispatchForm(forms.ModelForm):
    class Meta:
        model = DispatchLogt

        fields = [
            'name',
            'address',
            'deactivate',
            'date_deactivated',
        ]
        labels = {
            'name': 'Name:',
            'address': 'Address:',
            'deactivate': 'Deactivate:',
            'date_deactivated': 'Deactivate Date:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md'}),
            'deactivate': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'date_deactivated': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),

        }