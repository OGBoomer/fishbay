from django.forms import ModelForm
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from .models import Account


class FishbaySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100, required=True, label='Password')


class AccountCreationForm(UserCreationForm):
    beta_code = forms.CharField(max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super(AccountCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = Account
        fields = ['email', 'password1', 'password2', 'beta_code']


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ['email', ]


class LoginForm(forms.Form):
    email = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=50)


SUB_CHOICES = [
    ('month', 'Mothly billed at $1,000,000 every month'),
    ('semi', 'Semi-Annual billed at 5,400,000 every 6 months'),
    ('year', 'Annually billed at $10,200,000 every year'),
    ('beta', 'Free Beta Test account')
]


class SubscriptionForm(forms.Form):
    sub_term = forms.CharField(label='Length of subscription:', widget=forms.RadioSelect(choices=SUB_CHOICES))
    beta_code = forms.CharField(label='Beta invite code', max_length=30, required=False)

    def clean(self):
        beta_codes = ('DemoBeta', 'DailyBeta')
        cd = self.cleaned_data
        if cd['sub_term'] == 'beta' and cd['beta_code'] == '':
            raise ValidationError('Must have Beta Invite Code to join Beta Test')
        if cd['sub_term'] == 'beta' and cd['beta_code'] not in beta_codes:
            raise ValidationError('Invalid Invite Code')
        return cd
