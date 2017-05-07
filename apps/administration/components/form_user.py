from django import forms

from apps.administration.models import Users

class UserForm(forms.ModelForm):

    class Meta:
        model = Users

        fields = [
            'name',
            'lastname',
            'email',
            'password',
            'active',
            'profilers',
        ]
        labels = {
            'name' : 'Name',
            'lastname' : 'Last Name',
            'email' : 'Email',
            'password' : 'Password',
            'active' : 'Active',
            'profilers' : 'Profiler',
        }
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control input-md'}),
            'lastname': forms.TextInput(attrs={'class':'form-control input-md'}),
            'email': forms.EmailInput(attrs={'class':'form-control input-md'}),
            'password': forms.PasswordInput(attrs={'class':'form-control input-md'}),
            'active': forms.CheckboxInput(attrs={'class':'form-control input-md'}),
            'profilers': forms.Select(attrs={'class':'form-control input-md'}),
        }