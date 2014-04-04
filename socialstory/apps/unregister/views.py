#-*- coding:utf-8 -*-
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from apps.unregister.forms import MyRegistrationForm
from django.core.context_processors import csrf
from utils.decorators import render_to

def index(request):
    if request.user is not None:
        if request.user.is_active:
            return HttpResponseRedirect('/stories/')
        else:
            return HttpResponseRedirect('/acc/login/')
    else:
        return HttpResponseRedirect('/acc/login/')

@render_to('login.html')
def login(request):
    c = {}
    c.update(csrf(request))
    return c

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    #user.set_password(password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect('/writer/')
        else:
            return HttpResponseRedirect('/acc/login/')
    return HttpResponseRedirect('/acc/login/')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/acc/login/')

@render_to('register.html')
def register_user(request):
    errors = ''
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/acc/login/')
        errors = 'Дані введені невірно. Введіть ще раз.'
    args={}
    args.update(csrf(request))
    args['errors'] = errors
    return args