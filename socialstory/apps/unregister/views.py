import json
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from apps.unregister.forms import MyRegistrationForm
from django.core.context_processors import csrf

def render_to(template_path, allow_ajax=False):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            kwargs = {'context_instance': RequestContext(request)}

            if allow_ajax and request.is_ajax():
                return HttpResponse(json.dumps(output), 'application/json')

            if 'MIME_TYPE' in output:
                kwargs['mimetype'] = output.pop('MIME_TYPE')
            template = template_path
            if 'TEMPLATE' in output:
                template = output.pop('TEMPLATE')
            return render_to_response(template, output, **kwargs)
        return wrapper
    return decorator

def index(request):
    if request.user is not None:
        if request.user.is_active:
            return HttpResponseRedirect('/writer/')
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
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/acc/login/')
    args={}
    args.update(csrf(request))
    args['form'] = MyRegistrationForm()
    return args