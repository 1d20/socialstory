#-*- coding:utf-8 -*-
from django.db import models

class Writer(models.Model):
    user = models.OneToOneField('auth.User',primary_key=True)
    picture = models.ImageField(upload_to='user_pictures',default='user_pictures/default.jpg')
    status = models.CharField(max_length=65, default='')
    biography = models.TextField(default='')
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.user.username

class Comments(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_comment')
    story = models.ForeignKey('stories.Story', related_name='story_comment')
    paragraph_index = models.IntegerField(max_length=10, default=0)
    first_char = models.IntegerField(max_length=10, default=0)
    length = models.IntegerField(max_length=10, default=0)
    content = models.TextField(default='')
    color = models.CharField(max_length=15, default='')
    like_writer = models.BooleanField(default=False)
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.user.username+self.story.title+str(self.paragraph_index)

class WriterVote(models.Model):
    user = models.ForeignKey('auth.User', related_name='writer_vote')
    story = models.ForeignKey('stories.Story', related_name='story_vote')
    count = models.IntegerField(default=1)
    def __unicode__(self):
        return self.user.username+self.story.title+self.count

class WriterFavorite(models.Model):
    user = models.ForeignKey('auth.User', related_name='writer_favorite')
    story = models.ForeignKey('stories.Story', related_name='story_favorite')
    def __unicode__(self):
        return self.user.username+self.story.title

class WriterRead(models.Model):
    user = models.ForeignKey('auth.User', related_name='writer_read')
    story = models.ForeignKey('stories.Story', related_name='story_read')
    def __unicode__(self):
        return self.user.username+self.story.title

class Friends(models.Model):
    user1 = models.ForeignKey('auth.User', related_name='user_friend_1')
    user2 = models.ForeignKey('auth.User', related_name='user_friend_2')
    def __unicode__(self):
        return self.user1.username+self.user2.username

class Messages(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='user_message_from')
    user_to = models.ForeignKey('auth.User', related_name='user_message_to')
    content = models.TextField(default='')
    is_write = models.BooleanField(default=False)
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.user_from.username+self.user_to.username

class Setting(models.Model):
    title = models.CharField(max_length=255,default='')
    def __unicode__(self):
        return self.title

class SettingValue(models.Model):
    setting = models.ForeignKey('writer.Setting', related_name='setting_settingvalue')
    title = models.CharField(max_length=255,default='')
    def __unicode__(self):
        return self.setting+self.title

class UserSettings(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_usersetting')
    setting = models.ForeignKey('writer.SettingValue', related_name='settingvalue_usersetting')
    def __unicode__(self):
        return self.user.username+self.setting