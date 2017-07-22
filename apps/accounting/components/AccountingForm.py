from django import forms
from apps.accounting.models import *
from apps.logistic.models import InvoicesHasLoad, LoadsHasFee
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
            'fullname': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control input-md capital'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name', 'class': 'form-control input-md capital'}),
            'no_social': forms.NumberInput(attrs={'placeholder': 'SSN', 'class': 'form-control input-md'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Telepone Number', 'class': 'form-control input-md'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control input-md'}),
            'business': forms.Select(attrs={'class': 'form-control input-md'}),
            'deactivated': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'usdot': forms.NumberInput(attrs={'placeholder': 'USDOT Number', 'class': 'form-control input-md'}),
            'mc': forms.NumberInput(attrs={'placeholder': 'MC Number', 'class': 'form-control input-md'}),
            'txdmv': forms.TextInput(attrs={'placeholder': 'TXDMV Number', 'class': 'form-control input-md'}),
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
            'social_no': forms.NumberInput(attrs={'placeholder': 'Social Security', 'class': 'form-control input-md', 'required': 'true'}),
            'date_admis': forms.DateInput(attrs={'placeholder': 'Admission Date', 'class': 'form-control input-md'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Phone', 'class': 'form-control input-md'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control input-md', 'required': 'true'}),
            'type_salary': forms.Select(attrs={'class': 'form-control input-md'},choices=(('pervent','Commission'),('salary','Salary'))),
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
                'subtotal': 'Subtotal:',
                'total': 'Total:',
            }
            widgets = {
                'customers': forms.Select(attrs={'class': 'form-control input-md'}),
                'business': forms.Select(attrs={'class': 'form-control input-md'}),
                'start_date': forms.DateInput(attrs={'placeholder': 'Start Date', 'class': 'form-control input-md'}),
                'waytopay': forms.Select(attrs={'class': 'form-control input-md'},choices=(('Cash','Cash'),('Check','Check'),('Credit Card','Credit Card'))),
                'paid': forms.CheckboxInput(attrs={'class': 'checkbox'}),
                'prefix': forms.TextInput(attrs={'placeholder': 'Prefix', 'class': 'form-control input-md'}),
                'end_date': forms.DateInput(attrs={'placeholder': 'End Date', 'class': 'form-control input-md'}),
                'discount': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control discount'}),
                'subtotal': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control servSutotal', 'readonly':''}),
                'total': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control serviTotal', 'readonly':''}),
            }

class ItemHasInvoiceForm(forms.ModelForm):
    class Meta:
        model = InvoicesHasItem
        fields = {
            'id_ind',
            'quantity',
            'description',
            'accounts',
            'value',
            'tax',
            'subtotal',
        }
        widgets = {
            'id_ind': forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control', 'style':'display : none'}),
            'quantity': forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control entrada'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description ', 'class': 'form-control input-md descript'}),
            'accounts': forms.Select(attrs={'class': 'form-control input-md account', 'name': 'account'}),
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

class PaymentForm(forms.ModelForm):
       class Meta:
            model = Payment

            fields = [
                'accounts',
                'business',
                'start_date',
                'end_date',
                'serial',
                'discount',
                'value',
                'waytopay',
            ]
            widgets = {
                'accounts': forms.Select(attrs={'class': 'form-control input-md'}),
                'business': forms.Select(attrs={'class': 'form-control input-md'}),
                'start_date': forms.DateInput(attrs={'placeholder': 'Start Date', 'class': 'form-control input-md'}),
                'end_date': forms.DateInput(attrs={'placeholder': 'Start Date', 'class': 'form-control input-md'}),
                'discount': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control discount'}),
                'value': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control total', 'readonly': ''}),
                'waytopay': forms.Select(attrs={'class': 'form-control input-md'},
                                         choices=(('Cash', 'Cash'), ('Check', 'Check'), ('Credit Card', 'Credit Card'))),
            }


class InvoiceLoadForm(forms.ModelForm):
    class Meta:
        model = InvoicesHasLoad
        fields = {
            'id_inl',
            'loads',
        }
        widgets = {
            'id_inl': forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control', 'style': 'display : none'}),
            'loads': forms.Select(attrs={'class': 'form-control input-md load_id', 'name': 'load_id'}),
        }

class FeeLoadForm(forms.ModelForm):
    class Meta:
        model = LoadsHasFee
        fields = {
            'id_lfe',
            'fee',
            'value',

        }
        widgets = {
            'id_inl': forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control', 'style': 'display : none'}),
            'fee': forms.Select(attrs={'class': 'form-control input-md load_id', 'name': 'load_id'}),
            'value': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control fee-value', 'readonly': ''}),
        }


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = {
            'accounts',
            'description',
            'type',
            'value',

        }
        widgets = {
            'accounts': forms.Select(attrs={'class': 'form-control input-md', 'name': 'account'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control input-md'}),
            'type': forms.Select(attrs={'class': 'form-control input-md'},choices=(('pervent','Commission'),('salary','Salary'))),
            'value': forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control', 'style': 'display : none'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = {
            'note',
        }
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control fee-value'}),
        }