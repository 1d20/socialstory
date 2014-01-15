#-*- coding:utf-8 -*-
from django.db import models

class Story(models.Model):
    GENGES = (
        (1,u'Кіберпанк'),
        (2,u'Містика'),
        (3,u'Історія'),
        (4,u'Фантастика'),
        (5,u'Класика'),
        (6,u'Бойовик'),
        (7,u'Новела'),
        (8,u'Поезія'),
        (9,u'Детектив'),
        (10,u'Любовний роман'),
        (11,u'Наука'),
    )
    LANGUAGES = (
        (1,u'Українська'),
        (2,u'Російська'),
        (3,u'Англійська'),
        (4,u'Есперанто'),
        (5,u'Латинь'),
    )
    user = models.ForeignKey('auth.User', related_name='story_user')
    title = models.CharField(max_length=255)
    story = models.FileField(upload_to='stories', default='stories/default.txt')
    #from time import time
    #def someFunc(instance, filename):
    #    return "upload_files/%s_%s" % (str(time()).replace('.','_'), filename)
    # story = models.FileField(upload_to=someFunc)
    poster = models.ImageField(upload_to='posters', default='posters/default.jpg')
    description = models.TextField()
    rating = models.IntegerField(default=0)
    voteCount = models.IntegerField(default=0)
    pages = models.IntegerField(default=0)
    genge = models.IntegerField(max_length=2, choices=GENGES)
    language = models.IntegerField(max_length=2, choices=LANGUAGES)
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)

    def __unicode__(self):
        return u'%s: %s' % (self.user, self.title)

    class Meta:
        unique_together = ('user', 'title')
