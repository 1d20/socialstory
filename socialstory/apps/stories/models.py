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
    genres = models.ManyToManyField(SubGenre, related_name='story_subgenre')
    rating = models.IntegerField(default=0)
    voteCount = models.IntegerField(default=0)
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return str(self.id)

class Language(models.Model):
    language = models.CharField(max_length=255,default='')
    def __unicode__(self):
        return self.language

class SimilarStory(models.Model):
    story1 = models.ForeignKey(Story, related_name='similar_story_1')
    story2 = models.ForeignKey(Story, related_name='similar_story_2')
    count = models.IntegerField(max_length=10,default=0)
    def __unicode__(self):
        return str(self.story1)+' - '+str(self.story2)

class Branch(models.Model):
    language = models.ForeignKey('stories.Language', related_name='branch_language')
    story = models.ForeignKey(Story, related_name='story_version')
    user = models.ForeignKey('auth.User', related_name='user_version')
    title = models.CharField(max_length=100, default='')
    poster = models.ImageField(upload_to='posters', default='posters/default.jpg')
    description = models.TextField()
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)

    def pages(self):
        pages = []
        #pages.append(self.description)
        #pages.append(self.description)
        #pages.append(self.description)
        pages.append(self.description[:220])
        pages.append(self.description[221:440])
        pages.append(self.description[441:660])
        return pages
    class Meta:
        ordering = ['id']
    def __unicode__(self):
        return self.title

class BranchRequests(models.Model):
    branch = models.ForeignKey(Branch, related_name='branchrequest_branch')
    request_user = models.ForeignKey('auth.User', related_name='branchrequest_user')
    comment_message = models.TextField()
    def __unicode__(self):
        return self.branch.title+'- '+self.request_user.username

class Commit(models.Model):
    branch = models.ForeignKey(Branch, related_name='commit_branch')
    title = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=100, default='')
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.branch.title+self.title