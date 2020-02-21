from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    field_order = ['first_name', 'last_name',
                   'email', 'password1', 'password2']

    class Meta:
        model = User
        fields = ['email', 'password1',
                  'password2', 'first_name', 'last_name']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
