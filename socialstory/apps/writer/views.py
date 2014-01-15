import json
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from apps.writer.models import Writer
from apps.writer.forms import WriterForm
from django.core.context_processors import csrf

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