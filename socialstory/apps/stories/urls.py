#-*- coding: utf-8 -*-

from django.conf.urls import *
from apps.stories import views

urlpatterns = patterns('',
    url(r'^$', views.main, name='main'),
    url(r'^user/(?P<user_id>\d+)/$', views.user_stories, name='user_stories'),
    url(r'^user/fav/(?P<user_id>\d+)/$', views.user_fav_stories, name='user_fav_stories'),
    url(r'^user/trans/(?P<user_id>\d+)/$', views.user_trans_stories, name='user_trans_stories'),
    url(r'^all/$', views.all_stories, name='all_stories'),
    url(r'^best/$', views.best_stories, name='best_stories'),
    url(r'^votes/$', views.votes, name='votes'),
    url(r'^votes/(?P<user_id>\d+)/$', views.votes, name='votes'),
    url(r'^favorites/$', views.favorites, name='favorites'),
    url(r'^favorites/(?P<user_id>\d+)/$', views.favorites, name='favorites'),
    url(r'^reads/$', views.reads, name='reads'),
    url(r'^add/$', views.add_story, name='add_story'),
    url(r'^edit/(?P<branch_id>\d+)/$', views.edit_story, name='edit'),
    url(r'^editor/(?P<branch_id>\d+)/$', views.editor, name='editor'),
    url(r'^load/file/(?P<branch_id>\d+)/$', views.load_file, name='load_file'),
    url(r'^story/(?P<branch_id>\d+)/$', views.story, name='story'),
    url(r'^read/(?P<branch_id>\d+)/$', views.read, name='story'),
    url(r'^vote/(?P<story_id>\d+)/(?P<vote_count>\d+)/$', views.vote_story, name='vote'),
    url(r'^favorite/(?P<story_id>\d+)/$', views.favorite_story, name='favorite'),

    url(r'^branch/request/add/(?P<branch_id>\d+)/$', views.branch_request_add, name='branch_request_add'),
    url(r'^branch/add/(?P<req_id>\d+)/$', views.branch_add, name='branch_add'),

    url(r'^history/(?P<branch_id>\d+)/$', views.story_history, name='story_history'),
    url(r'^history/(?P<branch_id>\d+)/(?P<commit>\w+)/$', views.commit_info, name='commit_info'),
)
