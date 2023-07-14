from django.forms import ModelForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import Account
from .admin import UserCreationForm


class FishbaySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100, required=True, label='Password')


# class CreateAccountForm(UserCreationForm):
#     class Meta:
#         model = Account
#         fields = ['email', 'account', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=50)
