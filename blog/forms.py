from django.forms import ModelForm
from django import forms
from blog.models import Account


class SignUpForm(ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', 'last_name', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'email',
                'name': 'email',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'username',
                'name': 'username',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'name': 'password1',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name',
                'name': 'first_name',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name',
                'name': 'last_name',
            }),
        }
