from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, EditProfileForm, ProfileForm
from django.http import HttpResponseRedirect
from posts.models import Post
from django.views.defaults import page_not_found, server_error


def register(request):
    template = 'usersapp/register.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )

                user.save()

                login(request, user)
                return HttpResponseRedirect('/profile')
    else:
        form = RegisterForm()

    return render(request, template, {'form': form, 'title': 'Регистрация'})


def login_handler(request):
    template = 'usersapp/login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.data['username'], password=form.data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/profile')
            else:
                return render(request, template, {
                    'form': form,
                    'error_message': 'User not found.'
                })
    else:
        form = LoginForm()

    return render(request, template, {'form': form, 'title': 'Авторизация'})


def index(request):
    template = 'usersapp/index.html'
    return render(request, template, {'page_class': 'index-page', 'title': 'Главная'})


@login_required
def profile(request):
    template = 'usersapp/profile.html'

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/profile')
        # else:
        #     print(form.errors)
        #     return render(request, template, {'title': 'Профиль', 'form': form})
    else:
        usr_id = request.GET.get('user_id')
        usr = request.user if usr_id is None else User.objects.get(pk=usr_id)
        p = Post.objects.filter(author=usr).order_by('-created_date')
        posts_paginator = Paginator(p, 2)
        posts = posts_paginator.get_page(request.GET.get('page'))
        form = EditProfileForm()
        own = usr == request.user
        return render(request, template,
                      {'title': 'Профиль', 'form': form, 'posts': posts, 'posts_count': len(p), 'own': own, 'usr': usr})


def about(request):
    return render(request, 'usersapp/about.html', {'title': 'О нас'})


@login_required
def logout_handler(request):
    logout(request)
    return HttpResponseRedirect('/login')
