from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from apps.writer.forms import WriterForm
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
    return {'writer':Writer.objects.filter(user_id = user_id)[0], 'user_id':request.user.id }

@login_required
@render_to('edit_writer.html')
def edit_writer(request):
    if request.method == 'POST':
        form = WriterForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            writer = Writer.objects.get(user_id = request.user.id)
            writer.status=form.cleaned_data['status']
            if form.cleaned_data['picture'] == 'user_pictures/default.jpg':
                form.cleaned_data['picture'] = writer.picture
            writer.picture=form.cleaned_data['picture']
            writer.biography=form.cleaned_data['biography']
            writer.save()
            return HttpResponseRedirect('/')
    args={}
    args.update(csrf(request))
    writer = Writer.objects.filter(user_id = request.user.id)[0]
    writerForm = WriterForm(request.user, initial={
        'status': writer.status,
        'biography': writer.biography,
        'picture': writer.picture
    })
    args['form'] = writerForm#, Writer.objects.get(id=Writer.objects.filter(user_id = request.user.id)[0].id) )
    print args
    return args

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