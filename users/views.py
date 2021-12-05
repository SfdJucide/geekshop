from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages
from baskets.models import Basket
from users.models import User

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserProfileEditForm
from users.services import send_verify_email


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'GeekShop - Authorization',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, "You have successfully registered")
            send_verify_email(new_user)
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'GeekShop - Registration',
        'form': form
    }
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, files=request.FILES, data=request.POST)
        edit_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and edit_form.is_valid():
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        edit_form = UserProfileEditForm(instance=request.user.userprofile)

    context = {'title': 'GeekShop - profile',
               'form': form,
               'edit_form': edit_form,
               'baskets': Basket.objects.filter(user=request.user)}
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def verify(request, email, key):
    user = User.objects.filter(email=email).first()
    if user:
        if user.activate_key == key and not user.is_activate_key_expired():
            user.activate()
            auth.login(request, user)

    return render(request, 'users/register_result.html')
