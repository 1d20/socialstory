#-*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from apps.writer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>\d+)/$', views.writer, name='writer'),
    url(r'^edit/$', views.edit_writer, name='edit_writer'),
)
