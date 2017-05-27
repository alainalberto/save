from django import forms
from apps.logistic.models import *



class LoadsForm(forms.ModelForm):
    class Meta:
        model = Load

        fields = [
            'broker',
            'place_loading',
            'loading_date',
            'place_dischande',
            'dispash',
            'value',
            'number',
            'paid',
            'note',
        ]
        labels = {
            'broker': 'Broker Name:',
            'place_loading': 'Pick up From:',
            'loading_date': 'Pick up Date:',
            'place_dischande': 'Deliver to:',
            'dispash': 'Dispasher:',
            'value': 'Agreed Amount:',
            'number': 'Load Number:',
            'paid': 'Paid:',
            'note': 'Note:',
        }
        widgets = {
            'broker': forms.TextInput(attrs={'placeholder': 'Broker', 'class': 'form-control input-md'}),
            'place_loading': forms.TextInput(attrs={'placeholder': 'Pick up From', 'class': 'form-control input-md'}),
            'loading_date': forms.DateTimeInput(attrs={'class': 'form-control input-md'}),
            'place_dischande': forms.TextInput(attrs={'placeholder': 'Deliver to', 'class': 'form-control input-md'}),
            'dispash': forms.TextInput(attrs={'placeholder': 'Dispash', 'class': 'form-control input-md'}),
            'value': forms.NumberInput(attrs={'placeholder': 'Value', 'class': 'form-control input-md'}),
            'number': forms.TextInput(attrs={'placeholder': 'Number', 'class': 'form-control input-md'}),
            'paid': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'Note': forms.Textarea(attrs={'placeholder': 'Note about to', 'class': 'form-control input-md'}),

        }
