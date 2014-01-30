from django.contrib.auth.models import User
from apps.writer.models import Writer
from apps.stories.models import Story
from rest_framework import serializers

class WriterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Writer
        fields = ('id', 'user', 'picture', 'status', 'biography', 'date_add')

class StoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'user', 'title', 'story', 'poster', 'description', 'rating', 'voteCount', 'pages', 'genge',
                  'language', 'date_add')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')