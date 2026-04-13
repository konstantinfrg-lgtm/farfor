from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:collection_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            next_url = request.GET.get('next', 'catalog:collection_list')
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    context = {'form': form, 'title': 'Вход'}
    return render(request, 'accounts/auth_form.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('catalog:collection_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна! Добро пожаловать!')
            return redirect('catalog:my_collection')
    else:
        form = RegisterForm()

    context = {'form': form, 'title': 'Регистрация'}
    return render(request, 'accounts/auth_form.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('catalog:home')


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'Профиль обновлен!')
        return redirect('accounts:profile')

    user = request.user
    milk_jugs = user.milk_jugs.all()
    public_count = milk_jugs.filter(visibility='public').count()
    private_count = milk_jugs.filter(visibility='private').count()

    context = {
        'user': user,
        'public_count': public_count,
        'private_count': private_count,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def password_change(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = authenticate(username=request.user.username, password=old_password)
        if user is None:
            messages.error(request, 'Неверный текущий пароль.')
        elif new_password1 != new_password2:
            messages.error(request, 'Пароли не совпадают.')
        elif len(new_password1) < 8:
            messages.error(request, 'Пароль должен содержать не менее 8 символов.')
        else:
            user.set_password(new_password1)
            user.save()
            login(request, user)
            messages.success(request, 'Пароль успешно изменён!')
            return redirect('accounts:profile')

    return render(request, 'accounts/password_change.html', {})
