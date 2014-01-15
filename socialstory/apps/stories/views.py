#-*- coding:utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import StoryForm
from models import Story
from apps.writer.models import WriterVote, WriterFavorite, WriterRead

def render_to(template_path, allow_ajax=False):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            kwargs = {'context_instance': RequestContext(request)}

            if allow_ajax and request.is_ajax():
                return HttpResponse(json.dumps(output), 'application/json')

            if 'MIME_TYPE' in output:
                kwargs['mimetype'] = output.pop('MIME_TYPE')
            template = template_path
            if 'TEMPLATE' in output:
                template = output.pop('TEMPLATE')
            return render_to_response(template, output, **kwargs)
        return wrapper
    return decorator

@login_required
@render_to('stories.html')
def my_stories(request):
    return {'stories':Story.objects.filter(user_id = request.user.id), 'title':'Мої оповідання'}

@login_required
@render_to('stories.html')
def all_stories(request):
    return {'stories':Story.objects.filter().order_by('-date_add'), 'title':'Нові оповідання'}

@login_required
@render_to('stories.html')
def best_stories(request):
    return {'stories':Story.objects.filter().order_by('-rating'), 'title':'Кращі оповідання'}

@login_required
@render_to('stories.html')
def votes(request, user_id = 0):
    if user_id == 0: user_id = request.user.id
    def getStories(writer_vote): return Story.objects.get(id=writer_vote.story_id)
    votes = map(getStories,WriterVote.objects.filter(user_id = request.user.id))
    return {'stories':votes, 'title':'Проголосовані оповідання'}

@login_required
@render_to('stories.html')
def favorites(request, user_id = 0):
    if user_id == 0: user_id = request.user.id
    def getStories(writer_vote): return Story.objects.get(id=writer_vote.story_id)
    votes = map(getStories,WriterFavorite.objects.filter(user_id = request.user.id))
    return {'stories':votes, 'title':'Вибрані оповідання'}

@login_required
@render_to('stories.html')
def reads(request, user_id = 0):
    if user_id == 0: user_id = request.user.id
    def getStories(writer_vote): return Story.objects.get(id=writer_vote.story_id)
    votes = map(getStories,WriterRead.objects.filter(user_id = request.user.id))
    return {'stories':votes, 'title':'Переглянуті оповідання'}

@login_required
def main(request):
    return HttpResponseRedirect('/stories/my/')

@login_required
@render_to('add_story.html')
def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.user,request.POST, request.FILES)
        if form.is_valid():
            form.save() #commit=False
            return HttpResponseRedirect('/stories/my/')
    else:
        #form = StoryForm(request.user,instance=Story.objects.get(id=1))
        form = StoryForm(request.user)
    return { 'form': form, }

@login_required
@render_to('edit_story.html')
def edit_story(request, story_id=0):
    instance=Story.objects.get(id=story_id)
    if request.method == 'POST':
        form = StoryForm(request.user,request.POST, request.FILES)
        if form.is_valid():
            if instance.user_id != request.user.id:
                return HttpResponseRedirect('/stories/my/')
            form.save(story_id=story_id)
            return HttpResponseRedirect('/stories/story/'+str(story_id))
    else:
        if instance.user_id == request.user.id:
            form = StoryForm(request.user,instance=instance)
        else:
            return HttpResponseRedirect('/stories/my/')

    return { 'form': form,'story_id': instance.id, 'title':instance.title}

@login_required
@render_to('story.html')
def story(request, story_id=0):
    if not len(WriterRead.objects.filter(user_id=request.user.id,story_id=story_id)):
            WriterRead.objects.create(user_id=request.user.id,story_id=story_id)
    return {'story':Story.objects.filter(id = story_id)[0],
             'vote':not len(WriterVote.objects.filter(user_id=request.user.id,story_id=story_id)),
             'favorite':not len(WriterFavorite.objects.filter(user_id=request.user.id,story_id=story_id)),
             'my_story':len(Story.objects.filter(user_id=request.user.id,id=story_id))}

@login_required
def vote_story(request, story_id, vote_count):
    if story_id:
        if not len(WriterVote.objects.filter(user_id=request.user.id,story_id=story_id)):
            WriterVote.objects.create(user_id=request.user.id,story_id=story_id, count=vote_count)
            s = Story.objects.get(id=story_id)
            s.voteCount = s.voteCount + 1
            s.rating = s.rating + int(vote_count)
            s.save()
    return HttpResponseRedirect('/stories/story/'+str(story_id))

@login_required
def favorite_story(request, story_id):
    if story_id:
        if not len(WriterFavorite.objects.filter(user_id=request.user.id,story_id=story_id)):
            WriterFavorite.objects.create(user_id=request.user.id,story_id=story_id)
    return HttpResponseRedirect('/stories/story/'+str(story_id))