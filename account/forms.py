# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from account.models import Account


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("email",
                  "nick_name",
                  "password1",
                  "password2")


class AccountAuthenticationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError('E-Mail oder Passwort sind falsch.')


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ()
