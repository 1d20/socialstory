from django.db import models

class FriendsRequests(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='user_friend_request_from')
    user_to = models.ForeignKey('auth.User', related_name='user_friend_request_to')
    def __unicode__(self):
        return self.user_from.username+self.user_to.username

class Friends(models.Model):
    user1 = models.ForeignKey('auth.User', related_name='user_friend_1')
    user2 = models.ForeignKey('auth.User', related_name='user_friend_2')
    def __unicode__(self):
        return self.user1.username+self.user2.username