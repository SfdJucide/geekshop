from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'from-control py-4', 'placeholder': 'Enter user\'s name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'from-control py-4', 'placeholder': 'Enter password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'from-control py-4', 'placeholder': 'Enter user\'s name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'from-control py-4', 'placeholder': 'Enter email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'from-control py-4', 'placeholder': 'Enter name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'from-control py-4', 'placeholder': 'Enter surname'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'from-control py-4', 'placeholder': 'Enter user\'s name'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'from-control py-4', 'placeholder': 'Enter user\'s name'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')