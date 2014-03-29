from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from utils.decorators import render_to
from django.http import HttpResponse
import json
from apps.stories.models import *
from models import *

@login_required
def index(request):
    print request.user
    return HttpResponseRedirect('/writer/'+str(request.user.id)+'/')

@login_required
@render_to('writer.html')
def writer(request, user_id=1):
    count = 2
    comments = Comments.objects.filter(user=request.user)[:count]
    notes = Notes.objects.filter(user=request.user)[:count]
    marks = Marks.objects.filter(user=request.user)[:count]
    res = {
        'writer': Writer.objects.filter(user_id=user_id)[0],
        'user_id': request.user.id,
        'comments': comments,
        'notes': notes,
        'marks': marks,
    }
    return res

@login_required
@render_to('list.html')
def comments(request, user_id=1):
    comments = Comments.objects.filter(user_id=user_id)
    res = {
        'writer': Writer.objects.filter(user_id=user_id)[0],
        'show_path': 'writer/comments.html',
        'active_page': 'comments',
        'comments': comments,
    }
    return res

@login_required
@render_to('list.html')
def notes(request, user_id=1):
    notes = Notes.objects.filter(user_id=user_id)
    res = {
        'writer': Writer.objects.filter(user_id=user_id)[0],
        'show_path': 'writer/notes.html',
        'active_page': 'notes',
        'notes': notes,
    }
    return res

@login_required
@render_to('list.html')
def marks(request, user_id=1):
    marks = Marks.objects.filter(user_id=user_id)
    res = {
        'writer': Writer.objects.filter(user_id=user_id)[0],
        'show_path': 'writer/marks.html',
        'active_page': 'marks',
        'marks': marks,
    }
    return res

@login_required
@render_to('edit_writer.html')
def edit_writer(request):
    if request.method == 'POST':
        writer = Writer.objects.get(user_id=request.user.id)
        writer.user.first_name = request.POST.get('first_name')
        writer.user.last_name = request.POST.get('last_name')
        writer.user.username = request.POST.get('username')
        writer.status = request.POST.get('status')
        if request.FILES.get('picture'):
            writer.picture = request.FILES.get('picture')
        writer.biography = request.POST.get('biography')
        writer.user.save()
        writer.save()
        return HttpResponseRedirect('/writer/'+str(request.user.id))
    res = {
        'writer': Writer.objects.get(user_id = request.user.id)
    }
    res.update(csrf(request))
    return res

@login_required
def comment_add(request, branch_id=1):
    data = {'result': 'ok' }
    if request.method == 'POST':
        c = Comments()
        c.branch = Branch.objects.get(id = branch_id)
        c.user = request.user
        c.content = request.POST['content']
        c.paragraph_index = request.POST['paragraph_index']
        c.first_char = request.POST['first_char']
        c.last_char = request.POST['last_char']
        if request.POST.get('private'):
            c.private=True
        c.save()
    else:
        data = {'result': 'error(not POST request)' }
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def note_add(request, branch_id=1):
    data = {'result': 'ok'}
    if request.method == 'POST':
        n = Notes()
        n.branch = Branch.objects.get(id = branch_id)
        n.user = request.user
        n.content = request.POST['content']
        n.paragraph_index = request.POST['paragraph_index']
        n.save()
    else:
        data = {'result': 'error(not POST request)' }
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def mark_add(request, branch_id=1):
    data = {'result': 'ok' }
    if request.method == 'POST':
        m = Marks()
        m.branch = Branch.objects.get(id = branch_id)
        m.user = request.user
        m.paragraph_index = request.POST['paragraph_index']
        m.save()
    else:
        data = {'result': 'error(not POST request)' }
    return HttpResponse(json.dumps(data), content_type="application/json")