from django import forms
from apps.accounting.models import Accounts


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
