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
