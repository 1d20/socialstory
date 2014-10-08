#-*- coding: utf-8 -*-

from django.conf.urls import *
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^all/$', views.all_messages, name='all_messages'),
    url(r'^request/all/$', views.all_request, name='all_request'),
    url(r'^comments/all/$', views.all_comments, name='all_comments'),
    url(r'^request/delete/(?P<req_id>\d+)/$', views.delete_request, name='delete_request'),
    url(r'^write/(?P<user_id>\d+)/$', views.write_message, name='write_message'),
    url(r'^send/(?P<user_id>\d+)/$', views.send_message, name='send_message'),
)
