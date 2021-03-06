import hashlib

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from django.conf import settings

import pytz
from datetime import datetime

from users.models import User, UserProfile


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

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False

        user.activate_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
        user.activate_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()

        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')


class UserProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
