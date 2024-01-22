from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AccountRegisterForm(forms.ModelForm):
    USER_TYPES = (
        ('organizer', 'Organizer'),
        ('simple_user', 'Simple User'),
    )
    type_user = forms.ChoiceField(choices=USER_TYPES, required=True)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    profile_pic = forms.ImageField(required=False)  # Back to AccountRegisterForm

    class Meta:
        model = Account
        fields = ['type_user', 'full_name', 'phone_number', 'date_of_birth', 'profile_pic', 'address', 'bio']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['full_name', 'profile_pic','date_of_birth', 'phone_number', 'address', 'bio']
