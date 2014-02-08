from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from apps.writer.models import Writer
from apps.writer.forms import WriterForm
from django.core.context_processors import csrf
from utils.decorators import render_to

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