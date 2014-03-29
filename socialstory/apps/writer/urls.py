#-*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from apps.writer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>\d+)/$', views.writer, name='writer'),
    url(r'^edit/$', views.edit_writer, name='edit_writer'),

    url(r'^comments/(?P<user_id>\d+)/$', views.comments, name='comments'),
    url(r'^notes/(?P<user_id>\d+)/$', views.notes, name='notes'),
    url(r'^marks/(?P<user_id>\d+)/$', views.marks, name='marks'),

    url(r'^comment/add/(?P<branch_id>\d+)/$', views.comment_add, name='comment_add'),
    url(r'^note/add/(?P<branch_id>\d+)/$', views.note_add, name='note_add'),
    url(r'^mark/add/(?P<branch_id>\d+)/$', views.mark_add, name='mark_add'),
)
