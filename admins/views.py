from django.shortcuts import render, HttpResponseRedirect
from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda user: user.is_staff)
def index(request):
    context = {'title': 'GeekShop - Admin Panel'}
    return render(request, 'admins/index.html', context)


@user_passes_test(lambda user: user.is_staff)
def admin_users(request):
    context = {'title': 'Admin-Panel - Users',
               'users': User.objects.all()
               }
    return render(request, 'admins/admin-users-read.html', context)


@user_passes_test(lambda user: user.is_staff)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegistrationForm()
    context = {'title': 'Admin-Panel - Creation user',
               'form': form}
    return render(request, 'admins/admin-users-create.html', context)


@user_passes_test(lambda user: user.is_staff)
def admin_users_update(request, id):
    selected_user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserAdminProfileForm(instance=selected_user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminProfileForm(instance=selected_user)
    context = {'title': 'Admin-Panel - Edit user',
               'form': form,
               'selected_user': selected_user,
               }
    return render(request, 'admins/admin-users-update-delete.html', context)


@user_passes_test(lambda user: user.is_staff)
def admin_users_delete(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admins:admin_users'))
