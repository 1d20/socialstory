#-*- coding: utf-8 -*-

from django.conf.urls import *
from apps.people import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^friend/all/$', views.friend_all, name='friend_all'),
    url(r'^request/all/$', views.request_all, name='request_all'),
    url(r'^request/(?P<action>\w+)/(?P<user_to_id>\d+)/$', views.request, name='request'),
    url(r'^friend/(?P<action>\w+)/(?P<user_to_id>\d+)/$', views.friend, name='friend'),
    url(r'^all/$', views.all, name='all'),
)
