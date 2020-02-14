from django import forms
from django.contrib.auth.models import User
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


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50, validators=(validate_password,))

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=50, validators=(validate_username,))
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']