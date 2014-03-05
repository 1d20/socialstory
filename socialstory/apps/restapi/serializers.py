from django.contrib.auth.models import User
from apps.writer import models as WriterModel
from apps.stories import models as StoryModel
from apps.people import models as PeopleModel
from apps.messages import models as MessagesModel
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoryModel.Genre
        fields = ('id', 'title')

class SubGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoryModel.SubGenre
        fields = ('id', 'genre', 'title')

class StoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoryModel.Story
        fields = ('id', 'user', 'language', 'genres', 'title', 'story', 'poster', 'description', 'rating', 'voteCount',
                  'pages', 'date_add')

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoryModel.Language
        fields = ('id', 'language')

class SimilarStorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoryModel.SimilarStory
        fields = ('id', 'story1', 'story2', 'count')

class BranchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoryModel.Branch
        fields = ('id', 'story', 'user', 'title', 'date_add')

class CommitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoryModel.Commit
        fields = ('id', 'story', 'path', 'date_add')

class WriterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WriterModel.Writer
        fields = ('user', 'picture', 'status', 'biography', 'date_add')

class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WriterModel.Comments
        fields = ('id', 'user', 'story', 'paragraph_index', 'first_char', 'length', 'content', 'color', 'like_writer',
                  'date_add')

class WriterVoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WriterModel.WriterVote
        fields = ('id', 'user', 'story', 'count')

class WriterFavoriteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WriterModel.WriterFavorite
        fields = ('id', 'user', 'story')

class WriterReadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WriterModel.WriterRead
        fields = ('id', 'user', 'story')

class SettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WriterModel.Setting
        fields = ('id', 'title')

class SettingValueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WriterModel.SettingValue
        fields = ('id', 'setting', 'title')

class UserSettingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WriterModel.UserSettings
        fields = ('id', 'user', 'setting')

class FriendsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PeopleModel.Friends
        fields = ('id', 'user1', 'user2')

class FriendsRequestsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PeopleModel.FriendsRequests
        fields = ('id', 'user_from', 'user_to')

class MessagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MessagesModel.Messages
        fields = ('id', 'user_from', 'user_to', 'title', 'content', 'is_write', 'date_add')