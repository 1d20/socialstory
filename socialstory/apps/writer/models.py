#-*- coding:utf-8 -*-
from django.db import models

class Writer(models.Model):
    user = models.OneToOneField('auth.User', primary_key=True, related_name='writer_user')
    picture = models.ImageField(upload_to='user_pictures',default='user_pictures/default.jpg')
    status = models.CharField(max_length=65, default='')
    biography = models.TextField(default='')
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.user.username

class Comments(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_comment')
    branch = models.ForeignKey('stories.Branch', related_name='branch_comment')
    paragraph_index = models.IntegerField(max_length=10, default=0)
    first_char = models.IntegerField(max_length=10, default=0)
    last_char = models.IntegerField(max_length=10, default=0)
    content = models.TextField(default='')
    like_writer = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.user.username+self.branch.title+str(self.paragraph_index)

class Notes(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_notes')
    branch = models.ForeignKey('stories.Branch', related_name='branch_notes')
    paragraph_index = models.IntegerField(max_length=10, default=0)
    content = models.TextField(default='')
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.user.username+self.branch.title+str(self.paragraph_index)

class Marks(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_marks')
    branch = models.ForeignKey('stories.Branch', related_name='branch_marks')
    paragraph_index = models.IntegerField(max_length=10, default=0)
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.user.username+self.branch.title+str(self.paragraph_index)

class WriterVote(models.Model):
    user = models.ForeignKey('auth.User', related_name='writer_vote')
    story = models.ForeignKey('stories.Story', related_name='story_vote')
    count = models.IntegerField(default=1)
    def __unicode__(self):
        return self.user.username+str(self.count)

class WriterFavorite(models.Model):
    user = models.ForeignKey('auth.User', related_name='writer_favorite')
    story = models.ForeignKey('stories.Story', related_name='story_favorite')
    def __unicode__(self):
        return self.user.username

class WriterRead(models.Model):
    user = models.ForeignKey('auth.User', related_name='writer_read')
    story = models.ForeignKey('stories.Story', related_name='story_read')
    def __unicode__(self):
        return self.user.username

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