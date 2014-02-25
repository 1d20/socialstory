#-*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from apps.stories import views

urlpatterns = patterns('',
    url(r'^$', views.main, name='main'),
    url(r'^my/$', views.my_stories, name='my_stories'),
    url(r'^all/$', views.all_stories, name='all_stories'),
    url(r'^best/$', views.best_stories, name='best_stories'),
    url(r'^votes/$', views.votes, name='votes'),
    url(r'^votes/(?P<user_id>\d+)/$', views.votes, name='votes'),
    url(r'^favorites/$', views.favorites, name='favorites'),
    url(r'^favorites/(?P<user_id>\d+)/$', views.favorites, name='favorites'),
    url(r'^reads/$', views.reads, name='reads'),
    url(r'^add/$', views.add_story, name='add_story'),
    url(r'^edit/(?P<story_id>\d+)/$', views.edit_story, name='edit'),
    url(r'^editor/(?P<story_id>\d+)/$', views.editor, name='editor'),
    url(r'^story/(?P<story_id>\d+)/$', views.story, name='story'),
    url(r'^read/(?P<story_id>\d+)/$', views.read, name='story'),
    url(r'^vote/(?P<story_id>\d+)/(?P<vote_count>\d+)/$', views.vote_story, name='vote'),
    url(r'^favorite/(?P<story_id>\d+)/$', views.favorite_story, name='favorite'),
)
