from django import forms
from apps.accounting.models import *


class AccountForm(forms.ModelForm):
    class Meta:
        model = Accounts

        fields = [
            'name',
            'description',
            'accounts_id',
            'users',
        ]
        labels = {
            'name': 'Name:',
            'description': 'Description:',
            'accounts_id': 'Main Account:',
            'users': 'User:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control input-md'}),
            'accounts_id': forms.Select(attrs={'class': 'form-control input-md'}),
            'users': forms.Select(attrs={'class': 'form-control input-md'}),
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
            'name': 'Name:',
            'lastname': 'Last Name:',
            'no_social': 'SSN:',
            'address': 'Address:',
            'phone': 'Phone:',
            'email': 'Email:',
            'business': 'Busines:',
            'folders': 'Folders:',
            'users': 'User:',
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

class EmployeesForm(forms.ModelForm):
    class Meta:
        model = Employees

        fields = [
            'business',
            'name',
            'lastname',
            'adress',
            'social_no',
            'date_admis',
            'phone',
            'email',
            'type_salary',
            'value',
            'position',
        ]
        labels = {
            'business': 'Business:',
            'name': 'Name:',
            'lastname': 'Last Name:',
            'adress': 'Address:',
            'social_no': 'Social Security:',
            'date_admis': 'Admission Date:',
            'phone': 'Phone:',
            'email': 'Email:',
            'type_salary': 'Salary Type:',
            'value': 'Value:',
            'position': 'Position:',
        }
        widgets = {
            'business': forms.Select(attrs={'class': 'form-control input-md'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control input-md'}),
            'adress': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md'}),
            'social_no': forms.NumberInput(attrs={'placeholder': 'Social Security', 'class': 'form-control input-md'}),
            'date_admis': forms.DateTimeInput(attrs={'placeholder': 'Admission Date', 'class': 'form-control input-md'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Phone', 'class': 'form-control input-md'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control input-md'}),
            'type_salary': forms.TextInput(attrs={'placeholder': 'Salary Type', 'class': 'form-control input-md'}),
            'value': forms.NumberInput(attrs={'placeholder': 'Value', 'class': 'form-control input-md'}),
            'position': forms.TextInput(attrs={'placeholder': 'Position', 'class': 'form-control input-md'}),
        }

class InvoicesForm(forms.ModelForm):
        class Meta:
            model = Invoices

            fields = [
                'accounts',
                'customers',
                'business',
                'users',
                'serial',
                'start_date',
                'subtotal',
                'total',
                'waytopay',
                'discount',
                'paid',
                'prefix',
                'end_date',
            ]
            labels = {
                'accounts': 'Accounts:',
                'customers': 'Customers:',
                'business': 'Business:',
                'users': 'Users:',
                'serial': 'Serial:',
                'start_date': 'Start Date:',
                'subtotal': 'Subtotal:',
                'total': 'Total:',
                'waytopay': 'Way to Pay:',
                'discount': 'Discount:',
                'paid': 'Paid:',
                'prefix': 'Prefix:',
                'end_date': 'End Date:',
            }
            widgets = {
                'accounts': forms.Select(attrs={'class': 'form-control input-md'}),
                'customers': forms.Select(attrs={'class': 'form-control input-md'}),
                'business': forms.Select(attrs={'class': 'form-control input-md'}),
                'users': forms.Select(attrs={'class': 'form-control input-md'}),
                'serial': forms.NumberInput(attrs={'placeholder': 'Serial', 'class': 'form-control input-md'}),
                'start_date': forms.DateInput(attrs={'placeholder': 'Start Date', 'class': 'form-control input-md'}),
                'subtotal': forms.NumberInput(attrs={'placeholder': 'Subtotal', 'class': 'form-control input-md'}),
                'total': forms.NumberInput(attrs={'placeholder': 'Total', 'class': 'form-control input-md'}),
                'waytopay': forms.TextInput(attrs={'placeholder': 'Way to Pay', 'class': 'form-control input-md'}),
                'discount': forms.NumberInput(attrs={'placeholder': 'Discount', 'class': 'form-control input-md'}),
                'paid': forms.NumberInput(attrs={'placeholder': 'Paid', 'class': 'form-control input-md'}),
                'prefix': forms.TextInput(attrs={'placeholder': 'Prefix', 'class': 'form-control input-md'}),
                'end_date': forms.DateInput(attrs={'placeholder': 'End Date', 'class': 'form-control input-md'}),
            }


class InvoicesHasItemsForm(forms.ModelForm):
    class Meta:
        model = InvoicesHasItems

        fields = [
            'quantity_ind',
            'value_ind',
        ]
        labels = {
            'quantity_ind': 'Quantity',
            'value_ind': 'Value',
        }
        widgets = {
            'quantity_ind': forms.NumberInput(attrs={'placeholder': 'Quantity', 'class': 'form-control input-md'}),
            'value_ind': forms.TextInput(attrs={'placeholder': 'Value', 'class': 'form-control input-md'}),
        }