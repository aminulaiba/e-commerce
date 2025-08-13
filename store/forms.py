from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


twcssforinput = 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        # label="",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Email Address'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Username'
        })

        self.fields['password1'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Confirm Password'
        })


