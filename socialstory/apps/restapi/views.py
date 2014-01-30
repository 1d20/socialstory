from django.contrib.auth.models import User
from apps.writer.models import Writer
from apps.stories.models import Story
from rest_framework import viewsets
from serializers import WriterSerializer, StoriesSerializer, UserSerializer


class WriterViewSet(viewsets.ModelViewSet):
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer


class StoriesViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StoriesSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer