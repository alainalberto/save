from django import forms
from apps.accounting.models import *
from django.core.exceptions import ValidationError


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account

        fields = [
            'name',
            'description',
            'accounts_id',
        ]
        labels = {
            'name': 'Name:',
            'description': 'Description:',
            'accounts_id': 'Main Account:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control input-md'}),
            'accounts_id': forms.Select(attrs={'class': 'form-control input-md'}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer

        fields = [
            'fullname',
            'company_name',
            'no_social',
            'address',
            'phone',
            'email',
            'business',
            'deactivated',
            'usdot',
            'mc',
            'txdmv',
            'ein',
        ]
        labels = {
            'fullname': 'First and Last Name:',
            'company_name': 'Company Name:',
            'no_social': 'SSN:',
            'address': 'Address:',
            'phone': 'Phone:',
            'email': 'Email:',
            'business': 'Busines:',
            'deactivated': 'Deactivated:',
            'usdot': 'USDOT:',
            'mc': 'MC',
            'txdmv': 'Texas DMV:',
            'ein': 'EIN:',
        }
        widgets = {
            'fullname': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control input-md'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name', 'class': 'form-control input-md'}),
            'no_social': forms.NumberInput(attrs={'placeholder': 'SSN', 'class': 'form-control input-md'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Telepone Number', 'class': 'form-control input-md'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control input-md'}),
            'business': forms.Select(attrs={'class': 'form-control input-md'}),
            'deactivated': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'usdot': forms.NumberInput(attrs={'placeholder': 'USDOT Number', 'class': 'form-control input-md'}),
            'mc': forms.NumberInput(attrs={'placeholder': 'MC Number', 'class': 'form-control input-md'}),
            'txdmv': forms.NumberInput(attrs={'placeholder': 'TXDMV Number', 'class': 'form-control input-md'}),
            'ein': forms.NumberInput(attrs={'placeholder': 'EIN Number', 'class': 'form-control input-md'}),
        }


class EmployeesForm(forms.ModelForm):
    class Meta:
        model = Employee

        fields = [
            'business',
            'name',
            'lastname',
            'address',
            'social_no',
            'date_admis',
            'phone',
            'email',
            'type_salary',
            'value',
            'position',
            'deactivated',
        ]
        labels = {
            'business': 'Business:',
            'name': 'Name:',
            'lastname': 'Last Name:',
            'address': 'Address:',
            'social_no': 'Social Security:',
            'date_admis': 'Admission Date:',
            'phone': 'Phone:',
            'email': 'Email:',
            'type_salary': 'Salary Type:',
            'value': 'Value:',
            'position': 'Position:',
            'deactivated': 'Deactivated:',
        }
        widgets = {
            'business': forms.Select(attrs={'class': 'form-control input-md'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control input-md'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control input-md'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md'}),
            'social_no': forms.NumberInput(attrs={'placeholder': 'Social Security', 'class': 'form-control input-md'}),
            'date_admis': forms.DateTimeInput(attrs={'placeholder': 'Admission Date', 'class': 'form-control input-md'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Phone', 'class': 'form-control input-md'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control input-md'}),
            'type_salary': forms.TextInput(attrs={'placeholder': 'Salary Type', 'class': 'form-control input-md'}),
            'value': forms.NumberInput(attrs={'placeholder': 'Value', 'class': 'form-control input-md'}),
            'position': forms.TextInput(attrs={'placeholder': 'Position', 'class': 'form-control input-md'}),
            'deactivated': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }

        def clean_name(self):
            name = self.clean_data.get('name', '')
            num_words = len(name.split())
            if num_words < 4:
                raise forms.ValidationError("Not enough words!")
                return message

class InvoicesForm(forms.ModelForm):
        class Meta:
            model = Invoice

            fields = [
                'customers',
                'business',
                'start_date',
                'waytopay',
                'discount',
                'paid',
                'prefix',
                'end_date',
                'subtotal',
                'total',
            ]
            labels = {
                'customers': 'Customers:',
                'business': 'Business:',
                'start_date': 'Start Date:',
                'waytopay': 'Payment Method:',
                'discount': 'Discount:',
                'paid': 'Paid:',
                'prefix': 'Prefix:',
                'end_date': 'End Date:',
                'subtotal': 'Subtotal',
                'total': 'Total',
            }
            widgets = {
                'customers': forms.Select(attrs={'class': 'form-control input-md'}),
                'business': forms.Select(attrs={'class': 'form-control input-md'}),
                'start_date': forms.DateInput(attrs={'placeholder': 'Start Date', 'class': 'form-control input-md'}),
                 'waytopay': forms.Select(attrs={'class': 'form-control input-md'},choices=(('Cash','Cash'),('Check','Check'),('Credit Card','Credit Card'))),
                'paid': forms.CheckboxInput(attrs={'class': 'checkbox'}),
                'prefix': forms.TextInput(attrs={'placeholder': 'Prefix', 'class': 'form-control input-md'}),
                'end_date': forms.DateInput(attrs={'placeholder': 'End Date', 'class': 'form-control input-md'}),
                'discount': forms.NumberInput(attrs={'class': 'form-control  discount col-lg-9 col-md-6'}),
                'subtotal': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control servSutotal col-lg-9 col-md-6', 'readonly':''}),
                'total': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control serviTotal col-lg-9 col-md-6', 'readonly':''}),
            }

class ItemHasInvoiceForm(forms.ModelForm):
    class Meta:
        model = InvoicesHasItem
        fields = {
            'quantity',
            'description',
            'accounts',
            'value',
            'tax',
            'subtotal',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control entrada'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description ', 'class': 'form-control input-md descript'}),
            'accounts': forms.Select(attrs={'class': 'form-control input-md'}),
            'value': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control precie'}),
            'tax': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control tax'}),
            'subtotal': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control subtotal', 'readonly':''}),
        }

class ReceiptsForm(forms.ModelForm):
    class Meta:
        model = Receipt

        fields = [
            'business',
            'start_date',
            'waytopay',
            'paid',
            'end_date',
            'description',
            'total',
        ]
        labels = {
            'business': 'Business:',
            'start_date': 'Start Date:',
            'waytopay': 'Payment Method:',
            'paid': 'Paid:',
            'end_date': 'End Date:',
            'description': 'Description',
            'total': 'Total:',
        }
        widgets = {
            'business': forms.Select(attrs={'class': 'form-control input-md'}),
            'start_date': forms.DateInput(attrs={'placeholder': 'Start Date', 'class': 'form-control input-md'}),
            'waytopay': forms.Select(attrs={'class': 'form-control input-md'},
                                     choices=(('Cash', 'Cash'), ('Check', 'Check'), ('Credit Card', 'Credit Card'))),
            'paid': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'End Date', 'class': 'form-control input-md'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control input-md'}),
            'total': forms.NumberInput(attrs={'placeholder': 'Total', 'class': 'form-control input-md'}),
        }