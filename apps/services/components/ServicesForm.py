from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from apps.services.models import *
from apps.tools.models import File

class RelatedFieldWidgetCanAdd(forms.widgets.Select):

   def __init__(self, related_model, related_url=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
           rel_to = related_model
           info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
           related_url = 'admin:%s_%s_add' % info

        self.related_url = related_url

   def render(self, name, value, *args, **kwargs):
       accion = "window.open('/accounting/customers/create/1/','popup',' location=1, directories=0, resizable=0, width=500,height=700,Top=20,Left=490')"
       output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
       output.append(u'<span class="input-group-btn"><a type="button" onclick="%s" type="button" class="btn btn-success test-tooltip" id="add_id_%s"> ' % \
           (accion, name))
       output.append(u'<i class="fa fa-plus"></i><tooltip md-direction="right"></tooltip></a></span>')
       return mark_safe(u''.join(output))


class CompanyForm(forms.ModelForm):
    customers = forms.ModelChoiceField(
        required=True,
        queryset=Customer.objects.filter(deactivated=False),
        widget=RelatedFieldWidgetCanAdd(Customer, related_url="accounting:customer_create", attrs={'class': 'form-control input-md'})
    )
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
                  'logo',
                  'deactivate',
                  'state',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Company Name', 'class': 'form-control input-md upper'}),
            'attorney': forms.TextInput(attrs={'placeholder': 'Authorized Person:', 'class': 'form-control input-md upper'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control input-md upper'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Telepone Number', 'class': 'form-control input-md'}),
            'fax': forms.NumberInput(attrs={'placeholder': 'Fax Number', 'class': 'form-control input-md'}),
            'ein': forms.NumberInput(attrs={'placeholder': 'EIN', 'class': 'form-control input-md'}),
            'unity': forms.NumberInput(attrs={'placeholder': 'Unit', 'class': 'form-control input-md'}),
            'deactivate': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class PermitForm(forms.ModelForm):
    customers = forms.ModelChoiceField(
        required=True,
        queryset=Customer.objects.filter(deactivated=False),
        widget=RelatedFieldWidgetCanAdd(Customer, related_url="accounting:customer_create",
                                        attrs={'class': 'form-control input-md'})
    )
    class Meta:
        model = Permission

        fields = [
            'usdot',
            'usdot_pin',
            'txdmv',
            'txdmv_user',
            'txdmv_passd',
            'txdmv_date',
            'txdmv_date_exp',
            'mc',
            'mc_pin',
            'boc3',
            'boc3_date',
            'ucr',
            'state',
        ]
        labels = {
            'usdot': 'USDOT Number:',
            'usdot_pin': 'USDOT Pin:',
            'txdmv': 'TEXA DMV Number:',
            'txdmv_user': 'TEXA DMV User:' ,
            'txdmv_passd': 'TEXA DMV Password:',
            'txdmv_date': 'TEXA DMV Date:',
            'txdmv_date_exp': 'TEXA DMV Expiration:',
            'mc': 'MC Number: ',
            'mc_pin': 'MC Pin:',
            'boc3': 'BOC 3 Number:',
            'boc3_date': 'BOC 3 Date:',
            'ucr': 'URC:',
            'state': 'Service Process:',
        }
        widgets = {
            'usdot': forms.NumberInput(attrs={'placeholder': 'USDOT Number', 'class': 'form-control input-md'}),
            'usdot_pin': forms.TextInput(attrs={'placeholder': 'USDOT PIN', 'class': 'form-control input-md upper'}),
            'txdmv': forms.TextInput(attrs={'placeholder': 'TXDMV Number', 'class': 'form-control input-md upper'}),
            'txdmv_user': forms.TextInput(attrs={'placeholder': 'TXDMV User', 'class': 'form-control input-md'}),
            'txdmv_passd': forms.TextInput(attrs={'placeholder': 'TXDMV Password', 'class': 'form-control input-md'}),
            'txdmv_date': forms.DateInput(attrs={'placeholder': 'TXDMV Date', 'class': 'form-control input-md'}),
            'txdmv_date_exp': forms.DateInput(attrs={'placeholder': 'Exp Date', 'class': 'form-control input-md'}),
            'mc': forms.TextInput(attrs={'placeholder': 'MC Number', 'class': 'form-control input-md'}),
            'mc_pin': forms.TextInput(attrs={'placeholder': 'MC PIN', 'class': 'form-control input-md'}),
            'boc3': forms.TextInput(attrs={'placeholder': 'BOC3 Number', 'class': 'form-control input-md'}),
            'boc3_date': forms.DateInput(attrs={'placeholder': 'BOC3 Date', 'class': 'form-control input-md'}),
            'ucr': forms.NumberInput(attrs={'placeholder': 'USDOT Number', 'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class InsuranceForm(forms.ModelForm):
    customers = forms.ModelChoiceField(
        required=True,
        queryset=Customer.objects.filter(deactivated=False),
        widget=RelatedFieldWidgetCanAdd(Customer, related_url="accounting:customer_create",
                                        attrs={'class': 'form-control input-md'})
    )
    class Meta:
        model = Insurance

        fields = [
            'down_payment',
            'policy_efective_date',
            'policy_date_exp',
            'liability',
            'policy_liability',
            'cargo',
            'cargo_policy',
            'physical_damage',
            'physical_damg_policy',
            'sale_type',
            'sale_date_fee',
            'total',
            'comision',
            'paid',
            'state',
        ]
        labels = {
            'down_payment': 'Down Payment:',
            'policy_efective_date': 'Efective Date of Policy:',
            'policy_date_exp': 'Expire Date Policy:',
            'liability': 'Liability Value:',
            'policy_liability': 'Liability Policy Number:',
            'cargo': 'Cargo Value:',
            'cargo_policy': 'Cargo Policy Number:',
            'physical_damage': 'Physical Damage Value:',
            'physical_damg_policy': 'Physical Policy Number:',
            'sale_type': 'Sale Type:',
            'sale_date_fee': 'Sale Date Fee:',
            'total': 'Total:',
            'comision': 'Comision:',
            'paid': 'Is Paid:',
            'state':'Service Process:',
        }
        widgets = {
            'down_payment': forms.NumberInput(attrs={'placeholder': 'value Down', 'class': 'form-control input-md'}),
            'policy_efective_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'policy_date_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'liability': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'policy_liability': forms.TextInput(attrs={'placeholder': 'policy number', 'class': 'form-control input-md upper'}),
            'cargo': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'cargo_policy': forms.TextInput(attrs={'placeholder': 'policy number', 'class': 'form-control input-md upper'}),
            'physical_damage': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'physical_damg_policy': forms.TextInput(attrs={'placeholder': 'policy number', 'class': 'form-control input-md upper'}),
            'sale_type': forms.TextInput(attrs={'placeholder': 'type', 'class': 'form-control input-md'}),
            'sale_date_fee': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'total': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'comision': forms.NumberInput(attrs={'placeholder': 'value', 'class': 'form-control input-md'}),
            'paid': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class IftaForm(forms.ModelForm):
    customers = forms.ModelChoiceField(
        required=True,
        queryset=Customer.objects.filter(deactivated=False),
        widget=RelatedFieldWidgetCanAdd(Customer, related_url="accounting:customer_create",
                                        attrs={'class': 'form-control input-md'})
    )
    class Meta:
        model = Ifta

        fields = [
            'type',
            'period',
            'nex_period',
            'state',
        ]
        labels = {
            'type': 'Select Type:',
            'period': 'Select Period:',
            'nex_period': 'Date of nex Period: ',
        }
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Annual', 'Annual'), ('Quarter', 'Quarter'))),
            'period': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('Annual', 'Annual'), ('Quarter1', 'Quarter 1st'), ('Quarter2', 'Quarter 2nd'), ('Quarter3', 'Quarter 3rd'), ('Quarter4', 'Quarter 4th'))),
            'nex_period': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),

        }

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract


        fields = [
            'description',
            'serial',
            'start_date',
            'end_date',
            'type',
            'state',

        ]
        labels = {
            'description': 'Description:',
            'serial' : 'Serial',
            'start_date': 'Start Date:',
            'end_date': 'End Date:',
            'type': 'Type',

        }
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'serial': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'start_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'type': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class MTTForm(forms.ModelForm):
    customers = forms.ModelChoiceField(
        required=True,
        queryset=Customer.objects.filter(deactivated=False),
        widget=RelatedFieldWidgetCanAdd(Customer, related_url="accounting:customer_create",
                                        attrs={'class': 'form-control input-md'})
    )
    class Meta:
        model = Maintenance

        fields = [
            'nota',
            'state',

        ]
        labels = {
            'nota': 'Description of Maintenance:',
        }
        widgets = {
            'nota': forms.Textarea(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class TitleForm(forms.ModelForm):
    customers = forms.ModelChoiceField(
        required=True,
        queryset=Customer.objects.filter(deactivated=False),
        widget=RelatedFieldWidgetCanAdd(Customer, related_url="accounting:customer_create",
                                        attrs={'class': 'form-control input-md'})
    )
    class Meta:
        model = Title

        fields = [
            'date_reg',
            'date_exp_reg',
            'date_insp',
            'date_exp_insp',
            'trucks',
            'state',
        ]
        labels = {
            'date_reg': 'Register Date:',
            'date_exp_reg': 'Register Expire Date:',
            'date_insp': 'Inspection Date:',
            'date_exp_insp': 'Inspection Expire Date: ',
            'trucks': 'Trucks:',
        }
        widgets = {
            'date_reg': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'date_exp_reg': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'date_insp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'date_exp_insp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'trucks': forms.Select(attrs={'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class PlateForm(forms.ModelForm):
    customers = forms.ModelChoiceField(
        required=True,
        queryset=Customer.objects.filter(deactivated=False),
        widget=RelatedFieldWidgetCanAdd(Customer, related_url="accounting:customer_create",
                                        attrs={'class': 'form-control input-md'})
    )
    class Meta:
        model = Plate

        fields = [
            'date',
            'date_exp',
            'account_number',
            'account_user',
            'account_password',
            'trucks',
            'state',
        ]
        labels = {
            'date': 'Date:',
            'date_exp': 'Expire Date',
            'account_number': 'Account Number:',
            'account_user': 'Account User',
            'account_password': 'Account Password:',
            'trucks': 'Trucks:',
        }
        widgets = {
            'date': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'date_exp': forms.DateInput(attrs={'placeholder': 'Select date', 'class': 'form-control input-md'}),
            'account_number': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'account_user': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'account_password': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control input-md'}),
            'trucks': forms.Select(attrs={'class': 'form-control input-md'}),
            'state': forms.Select(attrs={'class': 'form-control input-md'}, choices=(
            ('Initiated', 'Initiated'), ('Pending', 'Pending'), ('Finalized', 'Finalized'))),
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = File

        fields = [
            'name',
            'category',
            'url',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name', 'class': 'form-control input-md upper'}),
            'category': forms.Select(attrs={'class': 'form-control input-md'}, choices=(('', '---------'),('Company', 'Company'), ('Insurance', 'Insurance'), ('Misselenious', 'Misselenious'))),
            'url': forms.FileInput(),
        }


