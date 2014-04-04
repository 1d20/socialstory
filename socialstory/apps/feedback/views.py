#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from models import FeedbackMessage
from utils.decorators import render_to

@login_required
@render_to('feedback.html')
def index(request):
    message_status = ''
    if request.method == "POST":
        message = FeedbackMessage()
        message.title = request.POST.get('title')
        message.content = request.POST.get('content')
        message.user = request.user
        message.save()
        message_status = 'Побажання прийнято. Дякуємо за співпрацю!'
    res = {'title': 'Побажання', 'message_status': message_status}
    res.update(csrf(request))
    return res
