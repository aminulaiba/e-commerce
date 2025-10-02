from django import forms
from .models import Shipping


twcssforinput = 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
twcssforcheckbox = 'form-checkbox h-3 w-3 text-blue-600 rounded focus:ring-blue-400 my-5'


class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Full Name'
        })
        self.fields['phone'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Phone'
        })
        self.fields['city'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'City'
        })
        self.fields['address_line_1'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Address'
        })
        self.fields['postal_code'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Post Code'
        })
        self.fields['is_default'].widget.attrs.update({
            'class': twcssforcheckbox,
        })
        self.fields['is_default'].label = "Default Address"

