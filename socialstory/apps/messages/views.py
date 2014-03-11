#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from models import Messages
from utils.decorators import render_to
from apps.stories.models import BranchRequests

@login_required
def index(request):
    return HttpResponseRedirect('/message/all/')

@login_required
@render_to('list.html')
def all_messages(request):
    return { 'title': 'Список повідомлень', 'messages': Messages.objects.filter(
            user_to=request.user).order_by('-date_add').all(), 'show_path': 'messages/all_messages.html',
             'active_page': 'all_messages' }

@login_required
@render_to('list.html')
def all_request(request):
    another_req = BranchRequests.objects.all()#filter(branch.story.user = request.user)
    my_req = BranchRequests.objects.filter(request_user = request.user)
    another_req = list(filter(lambda ar: ar.branch.story.user == request.user, another_req))
    #another_req = map(lambda u: u.user_to.writer, another_req)
    #my_req = map(lambda u: u.user_from.writer, my_req)
    return { 'title': 'Список запитів', 'show_path': 'messages/all_requests.html',
             'active_page': 'all_requests',
             'another_req': another_req,
             'my_req': my_req }

@login_required
@render_to('send_message.html')
def write_message(request, user_id):
    component = User.objects.get(id=user_id)
    mess_from = Messages.objects.filter(user_from = component, user_to = request.user).all()
    mess_to = Messages.objects.filter(user_to = component, user_from = request.user).all()
    messages = list(set(mess_from))
    for m in mess_to:
        messages.append(m)
    messages = sorted(messages, key=lambda messages: messages.date_add)
    messages = list(reversed(messages))
    res = { 'title': 'Відправити повідомлення', 'user': User.objects.get(id=user_id),
            'messages': messages }
    res.update(csrf(request))
    return res

@login_required
@render_to('send_message.html')
def send_message(request, user_id):
    if request.method == "POST":
        message = Messages()
        message.title = request.POST.get('title')
        message.content = request.POST.get('content')
        message.user_from = request.user
        message.user_to = User.objects.get(id=user_id)
        message.save()
        return HttpResponseRedirect('/message/all/')
    return HttpResponseRedirect('/message/write/'+user_id)