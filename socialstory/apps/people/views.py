#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from models import Friends, FriendsRequests
from apps.writer.models import Writer
from utils.decorators import render_to

@login_required
def index(request):
    return HttpResponseRedirect('/people/friend/all/')

@login_required
@render_to('people.html')
def friend_all(request):
    requests_user_friend1 = Friends.objects.filter(user1 = request.user.id)
    requests_user_friend2 = Friends.objects.filter(user2 = request.user.id)
    requests_user_friend1 = map(lambda u: u.user2.writer, requests_user_friend1)
    requests_user_friend2 = map(lambda u: u.user1.writer, requests_user_friend2)
    friends = list(set(requests_user_friend1))
    for u in requests_user_friend2:
        friends.append(u)
    return { 'title': 'Друзі', 'show_path': 'people/show_friends.html', 'active_page': 'friend_all',
             'friends': friends }

@login_required
@render_to('people.html')
def request_all(request):
    people_to = FriendsRequests.objects.filter(user_from = request.user)
    people_from = FriendsRequests.objects.filter(user_to = request.user)
    people_to = map(lambda u: u.user_to.writer, people_to)
    people_from = map(lambda u: u.user_from.writer, people_from)
    return { 'title': 'Заявки', 'show_path': 'people/show_request.html',
             'active_page': 'request_all',
             'people_to': people_to,
             'people_from': people_from }

@login_required
@render_to('people.html')
def all(request):
    requests_user_to = FriendsRequests.objects.filter(user_to = request.user)
    requests_user_from = FriendsRequests.objects.filter(user_from = request.user)
    requests_user_friend1 = Friends.objects.filter(user1 = request.user.id)
    requests_user_friend2 = Friends.objects.filter(user2 = request.user.id)

    requests_user_from = map(lambda u: u.user_to, requests_user_from)
    requests_user_to = map(lambda u: u.user_from, requests_user_to)
    requests_user_friend1 = map(lambda u: u.user2, requests_user_friend1)
    requests_user_friend2 = map(lambda u: u.user1, requests_user_friend2)

    another_users = Writer.objects.exclude(user=request.user).exclude(user__in=requests_user_to)\
        .exclude(user__in=requests_user_from).exclude(user__in=requests_user_friend1)\
        .exclude(user__in=requests_user_friend2).all()
    return { 'title': 'Всі', 'people': another_users, 'show_path': 'people/show_all.html',
             'active_page': 'all' }

@login_required
def request(request, action, user_to_id):
    if 'add' in action:
        FriendsRequests(user_from=request.user, user_to=User.objects.get(id=user_to_id)).save()
        return HttpResponseRedirect('/people/all/')
    if 'delete' in action:
        FriendsRequests.objects.filter(user_from=request.user, user_to=User.objects.get(id=user_to_id)).delete()
        FriendsRequests.objects.filter(user_to=request.user, user_from=User.objects.get(id=user_to_id)).delete()
        return HttpResponseRedirect('/people/request/all/')

@login_required
def friend(request, action, user_to_id):
    if 'add' in action:
        Friends(user1=request.user, user2=User.objects.get(id=user_to_id)).save()
        FriendsRequests.objects.filter(user_from=request.user, user_to=User.objects.get(id=user_to_id)).delete()
        FriendsRequests.objects.filter(user_to=request.user, user_from=User.objects.get(id=user_to_id)).delete()
        return HttpResponseRedirect('/people/request/all/')
    if 'delete' in action:
        Friends.objects.filter(user1=request.user, user2=User.objects.get(id=user_to_id)).delete()
        Friends.objects.filter(user2=request.user, user1=User.objects.get(id=user_to_id)).delete()
        return HttpResponseRedirect('/people/friend/all/')