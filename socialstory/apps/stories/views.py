#-*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from models import *
from apps.writer.models import *
from django.core.context_processors import csrf
from utils.decorators import render_to
from utils.file_module import *
from utils.git_module import *
from utils.story_module import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

def search_filter(stories, filter_string=''):
    ss = []
    for s in stories:
        for b in s.story_version.all():
            if filter_string in b.title:
                ss.append(s)
                break
    return ss

def get_subgenres(selected_genres=''):
    selSG = []
    if not selected_genres:
        allSG = SubGenre.objects.order_by('genre')
    else:
        selSG = selected_genres.split(',')[:-1]
        allSG = SubGenre.objects.order_by('genre').exclude(id__in=selSG)
        selSG = SubGenre.objects.filter(id__in=selSG).order_by('genre').all()
    return { 'subgenres': allSG, 'selected_subgenres': selSG }

def get_subgenres_and_stories(selected_genres='', sorted_by='-date_add', page=None, fitler_string=''):
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

    stories = search_filter(stories, fitler_string)
    paginator = Paginator(stories, 10)
    try:
        stories_list = paginator.page(page)
    except PageNotAnInteger:
        stories_list = paginator.page(1)
    except EmptyPage:
        stories_list = paginator.page(paginator.num_pages)
    return {'subgenres': allSG, 'selected_subgenres': selSG, 'stories': stories_list}

@login_required
@render_to('stories.html')
def user_stories(request, user_id=1):
    ss = Story.objects.filter(user_id=user_id).all()
    paginator = Paginator(ss, 10)
    try:
        stories_list = paginator.page(request.POST.get('page'))
    except PageNotAnInteger:
        stories_list = paginator.page(1)
    except EmptyPage:
        stories_list = paginator.page(paginator.num_pages)
    res = {'stories': stories_list,
            'title': 'Авторські оповідання '+str(Writer.objects.filter(user_id=user_id).all()[0].user.username), }
    res.update(get_subgenres(request.POST.get('genres')))
    res.update(csrf(request))
    return res

@login_required
@render_to('stories.html')
def user_fav_stories(request, user_id=1):
    wfs = WriterFavorite.objects.filter(user_id=user_id).all()
    ss = map(lambda wf: wf.story , wfs)
    paginator = Paginator(ss, 10)
    try:
        stories_list = paginator.page(request.POST.get('page'))
    except PageNotAnInteger:
        stories_list = paginator.page(1)
    except EmptyPage:
        stories_list = paginator.page(paginator.num_pages)
    res = {'stories': stories_list,
            'title': 'Вибрані оповідання '+str(Writer.objects.filter(user_id=user_id).all()[0].user.username), }
    res.update(get_subgenres(request.POST.get('genres')))
    res.update(csrf(request))
    return res

@login_required
@render_to('stories.html')
def user_trans_stories(request, user_id=1):
    bs = Branch.objects.filter(user_id=user_id).all()
    ss = []
    for b in bs:
        if b.story not in ss:
            ss.append(b.story)
    paginator = Paginator(ss, 10)
    try:
        stories_list = paginator.page(request.POST.get('page'))
    except PageNotAnInteger:
        stories_list = paginator.page(1)
    except EmptyPage:
        stories_list = paginator.page(paginator.num_pages)
    res = {'stories': stories_list,
            'title': 'Переклади '+str(Writer.objects.filter(user_id=user_id).all()[0].user.username), }
    res.update(get_subgenres(request.POST.get('genres')))
    res.update(csrf(request))
    return res

@login_required
@render_to('reader.html')
def read(request, branch_id=0):
    branch = Branch.objects.get(id = branch_id)
    content = get_last_publish_commit(branch)
    #print content
    res = {'content': content, 'branch':branch}
    res.update(csrf(request))
    return res

@login_required
@render_to('editor.html')
def editor(request, branch_id=0):
    branch = Branch.objects.get(id = branch_id)
    if branch.user != request.user:
        return HttpResponseRedirect('/stories/all/')
    if request.method == 'POST':
        print request.POST.get('content')
        content = request.POST.get('content')
        #print request.POST
        print request.POST.get('is_publish')
        rewrite_txt_content(branch, content)
        if request.POST.get('is_publish'):
            commit(branch, request.POST['commit_message'])
    content = get_txt_content(branch)
    res = {'content': content, 'story': branch}
    res.update(csrf(request))
    return res

@login_required
def load_file(request, branch_id=0):
    branch = Branch.objects.get(id = branch_id)
    if branch.user != request.user:
        return HttpResponseRedirect('/stories/all/')
    if request.method == 'POST':
        file = request.FILES.get('load_file')
        try:
            content = txt_to_ssr(file.readlines())
            rewrite_txt_content(branch, content)
        except:
            pass
    content = get_txt_content(branch)
    res = {'content': content, 'story': branch}
    res.update(csrf(request))
    return HttpResponseRedirect('/stories/editor/'+str(branch_id))

@login_required
@render_to('stories.html')
def all_stories(request):
    res = {'title': 'Нові оповідання', 'search': request.POST.get('search')}
    search = ''
    if request.POST.get('search'):
        search = request.POST.get('search')
    res.update(get_subgenres_and_stories(request.POST.get('genres'), '-date_add', request.POST.get('page'),
                                         search))
    res.update(csrf(request))
    return res

@login_required
@render_to('stories.html')
def best_stories(request):
    res = {'title': 'Кращі оповідання', 'request':request}
    res.update(get_subgenres_and_stories(request.POST.get('genres'), '-rating', request.POST.get('page')))
    res.update(csrf(request))
    return res

@login_required
@render_to('stories.html')
def votes(request, user_id=0):
    if user_id == 0: user_id = request.user.id
    def getStories(writer_vote): return Story.objects.get(id=writer_vote.story_id)
    votes = map(getStories,WriterVote.objects.filter(user_id = request.user.id))
    return {'stories': votes, 'title': 'Проголосовані оповідання'}

@login_required
@render_to('stories.html')
def favorites(request, user_id=0):
    if user_id == 0: user_id = request.user.id
    def getStories(writer_vote): return Story.objects.get(id=writer_vote.story_id)
    votes = map(getStories, WriterFavorite.objects.filter(user_id = request.user.id))
    return {'stories': votes, 'title': 'Вибрані оповідання'}

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
    res = {}
    if request.method == 'POST':
        print request.POST
        if not request.POST['title'] or not request.POST['description'] or not request.POST['language']\
            or not request.POST.get('story_subgenres') or not request.FILES.get('poster'):
            pass
        else:
            s = Story()
            s.user = request.user
            s.save()
            for g in request.POST.getlist('story_subgenres'):
                s.genres.add(SubGenre.objects.get(id=int(g)))
            b = Branch()
            b.language_id = int(request.POST['language'])
            b.story = s
            b.user = request.user
            b.title = request.POST['title']
            b.poster = request.FILES.get('poster')
            b.description = request.POST['description']
            b.save()
            create_branch(b)
            return HttpResponseRedirect('/stories/editor/'+str(b.id)+'/')

    res.update({ 'title':'Додати оповідання', 'languages':Language.objects.all(), 'all_subgenres':SubGenre.objects.all()})
    res.update(get_subgenres(request.POST.get('genres')))
    res.update(csrf(request))
    return res

@login_required
@render_to('add_story.html')
def branch_request_add(request, branch_id=0):
    b = Branch.objects.get(id=branch_id)
    br = BranchRequests()
    br.branch = b
    br.comment_message = request.POST['comment']
    br.request_user = request.user
    br.save()
    return HttpResponseRedirect('/stories/story/'+str(b.id)+'/')

@login_required
@render_to('add_branch.html')
def branch_add(request, req_id=0):
    req = BranchRequests.objects.get(id=req_id)
    if request.user != req.branch.story.user:
        return HttpResponseRedirect('/')
    res = {}
    if request.method == 'POST':
        if not request.POST['title'] or not request.POST['description'] or not request.POST['language']\
                or not request.FILES.get('poster'):
            pass
        else:
            b = Branch()
            b.language_id = int(request.POST['language'])
            b.story = req.branch.story
            b.user = req.request_user
            b.title = request.POST['title']
            b.poster = request.FILES.get('poster')
            b.description = request.POST['description']
            b.save()
            create_branch(b)
            content = get_last_publish_commit(req.branch)
            rewrite_txt_content(b, content)
            req.delete()
            return HttpResponseRedirect('/stories/editor/'+str(b.id)+'/')

    res.update({ 'title':'Нова гілка', 'languages':Language.objects.all(), 'request':req})
    res.update(csrf(request))
    return res

@login_required
@render_to('edit_story.html')
def edit_story(request, branch_id=0):
    branch = Branch.objects.get(id=branch_id)
    if request.method == 'POST':
        if not request.POST['title'] or not request.POST['description'] or not request.POST['language']:
            pass
        else:
            if branch.story.user_id != request.user.id:
                return HttpResponseRedirect('/stories/all/')
            branch.title = request.POST['title']
            branch.description = request.POST['description']
            branch.language.id = int(request.POST['language'])
            if request.FILES.get('poster'):
                branch.poster = request.FILES.get('poster')
            branch.save()
            return HttpResponseRedirect('/stories/story/'+str(branch.id))
    res = {'branch': branch, 'title': 'Редагування оповідання', 'languages':Language.objects.all()}
    res.update(get_subgenres(request.POST.get('genres')))
    res.update(csrf(request))
    return res

@login_required
@render_to('story.html')
def story(request, branch_id=0):
    branch = Branch.objects.get(id = branch_id)
    if not len(WriterRead.objects.filter(user_id=request.user.id,story_id=branch.story.id)):
            WriterRead.objects.create(user_id=request.user.id,story_id=branch.story.id)
    res = {
             'branch': branch,
             'vote': not len(WriterVote.objects.filter(user_id=request.user.id,story_id=branch.story.id)),
             'favorite': not len(WriterFavorite.objects.filter(user_id=request.user.id,story_id=branch.story.id)),
             'user': request.user,
             'similar_stories': get_similar_stories(branch),
          }
    res.update(get_subgenres(request.POST.get('genres')))
    res.update(csrf(request))
    return res

@login_required
def vote_story(request, story_id, vote_count):
    s = Story.objects.get(id=story_id)
    if not len(WriterVote.objects.filter(user_id=request.user.id,story_id=story_id)):
        WriterVote.objects.create(user_id=request.user.id,story_id=story_id, count=vote_count)
        s.voteCount += 1
        s.rating += int(vote_count)
        s.save()
    return HttpResponseRedirect('/stories/story/'+str(s.story_version.all()[0].id))

@login_required
def favorite_story(request, story_id):
    if story_id:
        if not len(WriterFavorite.objects.filter(user_id=request.user.id,story_id=story_id)):
            WriterFavorite.objects.create(user_id=request.user.id,story_id=story_id)
    s = Story.objects.get(id=story_id)
    return HttpResponseRedirect('/stories/story/'+str(s.story_version.all()[0].id))


@login_required
@render_to('story_history.html')
def story_history(request, branch_id=0):############################   history from story_id to branch_id
    branch = Branch.objects.get(id=branch_id)
    res = {'branch': branch}
    res.update(get_subgenres(request.POST.get('genres')))
    return res

@login_required
@render_to('commit_info.html')
def commit_info(request, branch_id=0, commit=0):
    commit = Commit.objects.get(id=commit)
    res = {'commit': commit, 'commit_info': get_commit_info(commit.branch, commit.code)}
    res.update(get_subgenres(request.POST.get('genres')))
    return res