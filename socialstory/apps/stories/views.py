#-*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from forms import StoryForm
from models import Story, SubGenre
from apps.writer.models import WriterVote, WriterFavorite, WriterRead
from django.core.context_processors import csrf
from utils.decorators import render_to
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_subgenres(selected_genres=''):
    selSG = []
    if not selected_genres:
        allSG = SubGenre.objects.order_by('genre')
    else:
        selSG = selected_genres.split(',')[:-1]
        allSG = SubGenre.objects.order_by('genre').exclude(id__in=selSG)
        selSG = SubGenre.objects.filter(id__in=selSG).order_by('genre').all()
    return { 'subgenres': allSG, 'selected_subgenres': selSG }

def get_subgenres_and_stories(selected_genres='', sorted_by='-date_add', page=None):
    stories = []
    selSG = []
    if not selected_genres:
        allSG = SubGenre.objects.order_by('genre')
        stories = Story.objects.filter().order_by(sorted_by)
    else:
        selSG = selected_genres.split(',')[:-1]
        allSG = SubGenre.objects.order_by('genre').exclude(id__in=selSG)
        selSG = SubGenre.objects.filter(id__in=selSG).order_by('genre').all()
        local_stories = []
        for ssg in selSG:
            for le in list(ssg.story_subgenre.all()):
                local_stories.append(le)
        for ls in local_stories:
            if ls not in stories:
                stories.append(ls)
        stories = sorted(stories, key=lambda stories: stories.date_add)
        stories = list(reversed(stories))

    paginator = Paginator(stories, 10)
    try:
        stories_list = paginator.page(page)
    except PageNotAnInteger:
        stories_list = paginator.page(1)
    except EmptyPage:
        stories_list = paginator.page(paginator.num_pages)
    return { 'subgenres': allSG, 'selected_subgenres': selSG, 'stories': stories_list }

@login_required
@render_to('stories.html')
def my_stories(request):
    return {'stories':Story.objects.filter(user_id = request.user.id), 'title':'Мої оповідання'}

@login_required
@render_to('stories.html')
def all_stories(request):
    res = {'title':'Нові оповідання'}
    res.update(get_subgenres_and_stories(request.POST.get('genres'), '-date_add', request.POST.get('page')))
    res.update(csrf(request))
    return res

@login_required
@render_to('stories.html')
def best_stories(request):
    res = {'title':'Кращі оповідання', 'request':request}
    res.update(get_subgenres_and_stories(request.POST.get('genres'), '-rating', request.POST.get('page')))
    res.update(csrf(request))
    return res

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
    return HttpResponseRedirect('/stories/all/')

@login_required
@render_to('add_story.html')
def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.user,request.POST, request.FILES)
        if form.is_valid():
            form.setUserId(request.user.id)
            form.save()
            return HttpResponseRedirect('/stories/all/')
    else:
        form = StoryForm(request.user)

    res = { 'form': form, 'title':'Додати оповідання'}
    res.update(get_subgenres(request.POST.get('genres')))
    res.update(csrf(request))
    return res

@login_required
@render_to('edit_story.html')
def edit_story(request, story_id=0):
    instance=Story.objects.get(id=story_id)
    if request.method == 'POST':
        form = StoryForm(request.user,request.POST, request.FILES)
        if form.is_valid():
            if instance.user_id != request.user.id:
                return HttpResponseRedirect('/stories/all/')
            form.setStoryData(story_id)
            form.setUserId(request.user.id)
            form.save()
            return HttpResponseRedirect('/stories/story/'+str(story_id))
    else:
        if instance.user_id == request.user.id:
            form = StoryForm(request.user,instance=instance)
        else:
            return HttpResponseRedirect('/stories/all/')
    res = { 'form': form, 'story_id': instance.id, 'title':instance.title}
    res.update(get_subgenres(request.POST.get('genres')))
    res.update(csrf(request))
    return res

@login_required
@render_to('story.html')
def story(request, story_id=0):
    if not len(WriterRead.objects.filter(user_id=request.user.id,story_id=story_id)):
            WriterRead.objects.create(user_id=request.user.id,story_id=story_id)
    res = {'story':Story.objects.filter(id = story_id)[0],
             'vote':not len(WriterVote.objects.filter(user_id=request.user.id,story_id=story_id)),
             'favorite':not len(WriterFavorite.objects.filter(user_id=request.user.id,story_id=story_id)),
             'my_story':len(Story.objects.filter(user_id=request.user.id,id=story_id))}
    res.update(get_subgenres(request.POST.get('genres')))
    res.update(csrf(request))
    return res

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