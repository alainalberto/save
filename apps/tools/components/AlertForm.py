from django import forms
from apps.tools.models import *
from django.contrib.auth.models import User, Group
from django.db.models.query_utils import DeferredAttribute


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert

        fields = [
            'category',
            'description',
            'show_date',
            'end_date',
            'deactivated',
            'group',
        ]
        labels = {
            'category': 'Category:',
            'description': 'Description:',
            'show_date': 'Show Date:',
            'end_date': 'End Date:',
            'deactivated': 'Deactivated:',
            'group': 'Group:',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Notification','Notification'), ('Alerts', 'Alerts'), ('Urgents', 'Urgents'))),
            'description': forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control input-md'}),
            'show_date': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'deactivated': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'group': forms.Select(attrs={'class': 'form-control input-md'}),
        }