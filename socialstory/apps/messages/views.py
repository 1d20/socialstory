#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from models import Messages
from utils.decorators import render_to
from apps.stories.models import BranchRequests
from apps.writer.models import *
from apps.stories.models import *

def get_messages(user):
    messages_tmp, messages = [], []
    ms1 = Messages.objects.filter(user_from = user).order_by('-date_add').all()
    ms2 = Messages.objects.filter(user_to = user).order_by('-date_add').all()
    for m in ms1:
        messages_tmp.append({
            'id': m.id,
            'user': m.user_to,
            'picture_url': m.user_to.writer_user.picture.url,
            'title': m.title,
            'content': m.content,
            'is_write': m.is_write,
            'date_add': m.date_add,
        })
    for m in ms2:
        messages_tmp.append({
            'id': m.id,
            'user': m.user_from,
            'picture_url': m.user_from.writer_user.picture.url,
            'title': m.title,
            'content': m.content,
            'is_write': m.is_write,
            'date_add': m.date_add,
        })

    messages_tmp = sorted(messages_tmp, key=lambda x: x['id'])
    messages_tmp = list(reversed(messages_tmp))

    user_ids = []
    for m in messages_tmp:
        if m['user'].id not in user_ids:
            user_ids.append(m['user'].id)
            messages.append(m)
    return messages

@login_required
def index(request):
    return HttpResponseRedirect('/message/all/')

@login_required
@render_to('list_messages.html')
def all_messages(request):

    res = { 'title': 'Список повідомлень', 'show_path': 'messages/all_messages.html',
             'active_page': 'all_messages' }
    res.update({'messages': get_messages(request.user)})
    return res

@login_required
@render_to('list_messages.html')
def all_request(request):
    another_req = BranchRequests.objects.all()
    my_req = BranchRequests.objects.filter(request_user = request.user)
    another_req = list(filter(lambda ar: ar.branch.story.user == request.user, another_req))
    return { 'title': 'Список запитів', 'show_path': 'messages/all_requests.html',
             'active_page': 'all_requests',
             'another_req': another_req,
             'my_req': my_req }

@login_required
@render_to('list_messages.html')
def all_comments(request):
    branches = Branch.objects.filter(user = request.user).all()
    comments = []
    for b in branches:
        cs = Comments.objects.filter(branch=b, like_writer=False, private=False).all()
        for c in cs:
            comments.append({
                'id': c.id,
                'paragraph_index': c.paragraph_index,
                'content': c.content,
                'date_add': c.date_add,
                'branch_title': c.branch.title,
                'writer_name': c.user.username,
                'writer_avatar': c.user.writer_user.picture.url,
            })

    changes = []
    for b in branches:
        cs = Comments.objects.filter(branch=b, like_writer=False, private=True).all()
        for c in cs:
            changes.append({
                'id': c.id,
                'paragraph_index': c.paragraph_index,
                'content': c.content,
                'date_add': c.date_add,
                'branch_title': c.branch.title,
                'writer_name': c.user.username,
                'writer_avatar': c.user.writer_user.picture.url,
            })
    res = {
        'show_path': 'messages/comments.html',
        'active_page': 'all_comments',
        'comments': comments,
        'changes': changes,
    }
    return res

@login_required
@render_to('send_message.html')
def write_message(request, user_id):###### new messages
    component = User.objects.get(id=user_id)
    mess_from = Messages.objects.filter(user_from = component, user_to = request.user).all()
    mess_to = Messages.objects.filter(user_to = component, user_from = request.user).all()
    messages = list(set(mess_from))
    for m in mess_to:
        m.is_write = True
        m.save()
        messages.append(m)
    for m in mess_from:
        messages.append(m)
    messages = sorted(messages, key=lambda messages: messages.date_add)
    messages = list(reversed(messages))
    ms = []
    for m in messages:
        ms.append({
            'id': m.id,
            'user': m.user_from,
            'picture_url': m.user_from.writer_user.picture.url,
            'title': m.title,
            'content': m.content,
            'is_write': m.is_write,
            'date_add': m.date_add,
        })
    res = { 'title': 'Відправити повідомлення', 'user': User.objects.get(id=user_id),
            'messages': ms }
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

@login_required
@render_to('list_messages.html')
def delete_request(request, req_id=0):
    req = BranchRequests.objects.get(id=req_id)
    if request.user == req.request_user or request.user == req.branch.story.user:
        req.delete()
    return HttpResponseRedirect('/message/request/all/')