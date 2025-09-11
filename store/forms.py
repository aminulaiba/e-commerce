from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile

twcssforinput = 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'

class PasswordChange(SetPasswordForm):

    class Meta:
        model=User
        fields = ['new_password1', 'new_password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'New Password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Confirm Password'
        })




class UpdateUserForm(UserChangeForm):
    password = None
    email = forms.EmailField(
        # label="",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Email Address'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Username'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'first name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'last name'
        })

# profile updating form
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Phone number'
        })
        self.fields['address'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'Address'
        })
        self.fields['city'].widget.attrs.update({
            'class': twcssforinput,
            'placeholder': 'City'
        })





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


