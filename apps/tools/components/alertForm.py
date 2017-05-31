from django import forms
from apps.tools.models import Alert


class alertForm(forms.ModelForm):
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
            'deactivated': 'Activated:',
            'group': 'Group:',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('#E74C3C','Notification'), ('#DC7633', 'Alerts'), ('#27AE60', 'Urgents'))),
            'description': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control input-md'}),
            'show_date': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control input-md'}),
            'deactivated': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'group': forms.Select(attrs={'class': 'form-control input-md'}),
        }