from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from custom_account.models import Account


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')