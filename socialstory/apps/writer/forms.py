# -*- coding: utf-8

#from django import forms
from django.forms import ModelForm
from models import Writer as WriterModel

class WriterForm(ModelForm):
    def __init__(self, user, *args, **kw):
        self.user = user
        super(WriterForm, self).__init__(*args, **kw)
    class Meta:
        model = WriterModel
        fields = ['picture', 'status', 'biography']
    def save(self, *args, **kwargs):
        self.instance.user_id = self.user.id
        self.instance.save()