from django import forms
from apps.services.models import *

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Companie

        fields = [
                  'name',
                  'attorney',
                  'address',
                  'phone',
                  'fax',
                  'ein',
                  'unity',
                  'deactivate',
        ]
        labels = {
                  'name': 'Company Name:',
                  'attorney': 'Attorney`s Name:',
                  'address': 'Address:',
                  'phone': 'Phone Number:',
                  'fax': 'Fax Number:',
                  'ein': 'EIN Number:',
                  'unity': 'Unity:',
                  'deactivate': 'Is Deactivate:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Company Name', 'class': 'form-control input-md'}),
            'attorney': forms.TextInput(attrs={'placeholder': 'Attorney', 'class': 'form-control input-md'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Telepone Number', 'class': 'form-control input-md'}),
            'fax': forms.NumberInput(attrs={'placeholder': 'Fax Number', 'class': 'form-control input-md'}),
            'ein': forms.NumberInput(attrs={'placeholder': 'EIN', 'class': 'form-control input-md'}),
            'unity': forms.NumberInput(attrs={'placeholder': 'SSN', 'class': 'form-control input-md'}),
            'deactivate': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }



