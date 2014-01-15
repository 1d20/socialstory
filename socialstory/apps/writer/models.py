#-*- coding:utf-8 -*-
from django.db import models

class Writer(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_writer')
    picture = models.ImageField(upload_to='user_pictures',default='user_pictures/default.jpg')
    status = models.CharField(max_length=65, default='')
    biography = models.TextField(default='')
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.user)

    class Meta:
        unique_together = ('user', 'date_add')


class WriterVote(models.Model):
    user = models.ForeignKey('auth.User', related_name='writer_vote')
    story = models.ForeignKey('stories.Story', related_name='story_vote')
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return u'%s' % (self.user)

    class Meta:
        unique_together = ('user', 'story')

class WriterFavorite(models.Model):
    user = models.ForeignKey('auth.User', related_name='writer_favorite')
    story = models.ForeignKey('stories.Story', related_name='story_favorite')

    def __unicode__(self):
        return u'%s' % (self.user)

    class Meta:
        unique_together = ('user', 'story')

class WriterRead(models.Model):
    user = models.ForeignKey('auth.User', related_name='writer_read')
    story = models.ForeignKey('stories.Story', related_name='story_read')

    def __unicode__(self):
        return u'%s' % (self.user)

    class Meta:
        unique_together = ('user', 'story')
