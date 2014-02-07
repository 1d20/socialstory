#-*- coding:utf-8 -*-
from django.db import models

class Genre(models.Model):
    title = models.CharField(max_length=255,default='')
    def __unicode__(self):
        return self.title

class SubGenre(models.Model):
    title = models.CharField(max_length=255,default='')
    genre = models.ForeignKey(Genre, related_name='genre_subgenre')
    def __unicode__(self):
        return self.title

class Story(models.Model):
    user = models.ForeignKey('auth.User', related_name='story_user')
    language = models.ForeignKey('stories.Language', related_name='story_language')
    genres = models.ManyToManyField(SubGenre, related_name='story_subgenre')
    title = models.CharField(max_length=255)
    story = models.FileField(upload_to='stories', default='stories/default.txt')
    poster = models.ImageField(upload_to='posters', default='posters/default.jpg')
    description = models.TextField()
    rating = models.IntegerField(default=0)
    voteCount = models.IntegerField(default=0)
    pages = models.IntegerField(default=0)
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.title

class Language(models.Model):
    language = models.CharField(max_length=255,default='')
    def __unicode__(self):
        return self.language

class SimilarStory(models.Model):
    story1 = models.ForeignKey(Story, related_name='similar_story_1')
    story2 = models.ForeignKey(Story, related_name='similar_story_2')
    count = models.IntegerField(max_length=10,default=0)
    def __unicode__(self):
        return self.story1+self.story2

class Versions(models.Model):
    story = models.ForeignKey(Story, related_name='story_version')
    path = models.FileField(upload_to='versions',default='default')
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.story+self.path