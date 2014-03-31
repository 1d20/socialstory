from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
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
    comments = Comments.objects.filter(user_id=user_id, like_writer=True)[:count]
    notes = Notes.objects.filter(user_id=user_id)[:count]
    marks = Marks.objects.filter(user_id=user_id)[:count]
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
    comments = Comments.objects.filter(user_id=user_id, like_writer=True)
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
        print request.POST.get('private')
        if request.POST.get('private'):
            c.private = True
        else:
            c.private = False

        #c.private = True
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
        print request.POST
        m = Marks()
        m.branch = Branch.objects.get(id = branch_id)
        m.user = request.user
        m.paragraph_index = request.POST['paragraph_index']
        m.save()
    else:
        data = {'result': 'error(not POST request)' }
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def comments_get(request, branch_id=1, paragraph_id=1):
    data = []
    comments = Comments.objects.filter(branch_id=branch_id, paragraph_index=paragraph_id, like_writer=True).all()
    for c in comments:
        data.append({
            'writer_name': c.user.username,
            'writer_avatar': c.user.writer_user.picture.url,
            'content': c.content,
            'date': str(c.date_add),
        })
    return HttpResponse(json.dumps({'data': data}), content_type="application/json")

@login_required
def comments_count(request, branch_id=1):
    data = []
    comments = Comments.objects.filter(branch_id=branch_id, like_writer=True).all()
    tmp = {}
    for c in comments:
        try:
            tmp[c.paragraph_index] += 1
        except:
            tmp[c.paragraph_index] = 1
    for t in tmp:
        data.append({
            'paragraph_index': t,
            'count': tmp[t],
        })

    return HttpResponse(json.dumps({'data': data}), content_type="application/json")

@login_required
def comment_submit_ok(request, comment_id=1):
    comment = Comments.objects.get(id=comment_id)
    comment.like_writer = True
    comment.save()
    return HttpResponseRedirect('/message/comments/all/')

@login_required
def comment_submit_no(request, comment_id=1):
    Comments.objects.get(id=comment_id).delete()
    return HttpResponseRedirect('/message/comments/all/')