from django.db import models

class FeedbackMessage(models.Model):
    user = models.ForeignKey('auth.User', related_name='feedback_user')
    title = models.TextField(default='')
    content = models.TextField(default='')
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)

    def __unicode__(self):
        return self.title+': '+self.content