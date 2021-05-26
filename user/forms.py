
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput
from django.utils.translation import gettext_lazy as _
from user.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label=_('User Name :'),widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(max_length=200, label=_('Email :'),widget=forms.TextInput(attrs={'class': 'input'}))
    first_name = forms.CharField(
        max_length=100,  label=_('First Name :'),widget=forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(
        max_length=100,  label=_('Last Name :'),widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(
        max_length=100, label=_('password :'),widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(
        max_length=100, label=_('password :'),widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2', ]
       

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': _('username')}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': _('email')}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': _('first_name')}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': _('last_name')}),
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': _('phone')}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': _('address')}),
            'city': Select(attrs={'class': 'input', 'placeholder': _('city')}, choices=CITY),
            'country': TextInput(attrs={'class': 'input', 'placeholder': _('country')}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': _('image'), }),
        }