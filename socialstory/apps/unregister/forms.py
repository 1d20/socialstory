#-*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from django.forms.models import modelform_factory
from apps.writer.models import Writer

#MyRegistrationForm = modelform_factory(User)

class MyRegistrationForm(UserCreationForm):
    #email = forms.EmailField(required=True, label=u'E-mail')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': (u'Writer'),
        }
        #help_texts = {
        #    'name': _('Some useful help text.'),
        #}
        #labels = {
        #    'username': u'Імя користувача',
        #    'email' :u'E-mail',
        #    'password1' :u'Пароль',
        #    'password2' :u'Повторіть пароль'
        #}

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        #user.email = self.changed_data['email']
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            Writer.objects.create(user=user)

        return user
