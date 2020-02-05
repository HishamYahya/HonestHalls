from django import forms
from .validators import (
    validate_email,
    validate_password,
    validate_username
)


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=50, validators=(validate_username,))
    password1 = forms.CharField(max_length=50, validators=(validate_password,))
    password2 = forms.CharField(max_length=50)
