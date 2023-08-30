from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .forms import AccountCreationForm, AccountChangeForm
from .models import Account, StripePayment


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        print(self.cleaned_data)
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('password', 'is_active', 'is_admin')


class AccountAdmin(UserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    model = Account

    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {
            'fields':
                ('email', 'password')
        }),
        ('Permissions', {
            'fields':
                ('is_staff', 'is_active')
        }),
        ('Myfishbay Fields', {
            'fields':
                ('status', 'stripe_cus_id', 'stripe_sub_id', 'sub_start', 'sub_expire', 'sub_auto_renew')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields':
                ('is_staff', 'is_active')
        }),
        ('Myfishbay Fields', {
            'fields':
                ('status', 'stripe_cus_id', 'stripe_sub_id', 'sub_start', 'sub_expire', 'sub_auto_renew')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Account, AccountAdmin)
admin.site.register(StripePayment)
admin.site.unregister(Group)
