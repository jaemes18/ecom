from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Full Name'}), required=False)
    shipping_email = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email Address'}), required=False)
    shipping_address1 = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address 1'}), required=False)
    shipping_address2 = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address 2'}), required=False)
    shipping_city = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'City'}), required=False)
    shipping_state = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'State'}), required=False)
    shipping_zip_code = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Zip_code'}), required=False)
    shipping_country = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Country'}), required=False)


    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name','shipping_email', 'shipping_address1', 'shipping_address2','shipping_city', 'shipping_state','shipping_zip_code','shipping_country']

        exclude = ['user', ]


class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Card Name'}), required=False)
    card_number = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Card Number'}), required=False)
    card_exp_date = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Expiration Date'}), required=False)
    card_cvv_number = forms.CharField(label="", widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'CVV Number'}), required=False)


