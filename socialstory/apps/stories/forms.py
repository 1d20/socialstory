# -*- coding: utf-8

from django import forms
from django.forms import ModelForm
from models import Story as StoryModel
from datetime import datetime
from django.forms.models import modelform_factory

#StoryForm = modelform_factory(StoryModel)

class StoryForm(ModelForm):
    def __init__(self, user, *args, **kw):
        self.user = user
        super(StoryForm, self).__init__(*args, **kw)
        #self.title.label = 'asd'
    class Meta:
        model = StoryModel
        exclude = ('user', )
        #fields='__all__'
        fields = ['title', 'description', 'language', 'poster', 'genres']
    def setUserId(self, user_id = 0):
        self.instance.user_id = user_id
    def setStoryData(self, story_id = 0):
        story = StoryModel.objects.get(id = story_id)
        self.instance.id = story.id
        self.instance.rating=story.rating
        self.instance.voteCount=story.voteCount
        self.instance.date_add = datetime.now()
    #def save(self, story_id=0, *args, **kwargs):
    #    self.instance.user_id = self.user.id
    #    if story_id != 0:
    #        story = StoryModel.objects.get(id = story_id)
    #        if self.cleaned_data['story'] == 'stories/default.txt':
    #            self.instance.story = story.story
    #        if self.cleaned_data['poster'] == 'posters/default.jpg':
    #            self.instance.poster = story.poster
    #        self.instance.id=story_id
    #        self.instance.rating=story.rating
    #        self.instance.voteCount=story.voteCount
    #        self.instance.date_add = datetime.now()
    #    self.instance.save()
        #self.instance.save_m2m()