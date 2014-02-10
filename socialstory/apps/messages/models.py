from django.db import models

class Messages(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='user_message_from')
    user_to = models.ForeignKey('auth.User', related_name='user_message_to')
    title = models.TextField(default='')
    content = models.TextField(default='')
    is_write = models.BooleanField(default=False)
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)
    def __unicode__(self):
        return self.user_from.username+self.user_to.username