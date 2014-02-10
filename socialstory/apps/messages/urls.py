#-*- coding: utf-8 -*-

from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^all/$', views.all_messages, name='all_messages'),
    url(r'^write/(?P<user_id>\d+)/$', views.write_message, name='write_message'),
    url(r'^send/(?P<user_id>\d+)/$', views.send_message, name='send_message'),
)
