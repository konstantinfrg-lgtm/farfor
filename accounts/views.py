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
    
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)
