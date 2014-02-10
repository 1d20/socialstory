from django.contrib.auth.models import User
from apps.writer import models as WriterModel
from apps.stories import models as StoryModel
from apps.people import models as PeopleModel
from apps.messages import models as MessageModel
from rest_framework import viewsets
import serializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = StoryModel.Genre.objects.all()
    serializer_class = serializers.GenreSerializer

class SubGenreViewSet(viewsets.ModelViewSet):
    queryset = StoryModel.SubGenre.objects.all()
    serializer_class = serializers.SubGenreSerializer

class StoriesViewSet(viewsets.ModelViewSet):
    queryset = StoryModel.Story.objects.all()
    serializer_class = serializers.StoriesSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = StoryModel.Language.objects.all()
    serializer_class = serializers.LanguageSerializer

class SimilarStoryViewSet(viewsets.ModelViewSet):
    queryset = StoryModel.SimilarStory.objects.all()
    serializer_class = serializers.SimilarStorySerializer

class VersionsViewSet(viewsets.ModelViewSet):
    queryset = StoryModel.Versions.objects.all()
    serializer_class = serializers.VersionsSerializer

class WriterViewSet(viewsets.ModelViewSet):
    queryset = WriterModel.Writer.objects.all()
    serializer_class = serializers.WriterSerializer

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = WriterModel.Comments.objects.all()
    serializer_class = serializers.CommentsSerializer

class WriterVoteViewSet(viewsets.ModelViewSet):
    queryset = WriterModel.WriterVote.objects.all()
    serializer_class = serializers.WriterVoteSerializer

class WriterFavoriteViewSet(viewsets.ModelViewSet):
    queryset = WriterModel.WriterFavorite.objects.all()
    serializer_class = serializers.WriterFavoriteSerializer

class WriterReadViewSet(viewsets.ModelViewSet):
    queryset = WriterModel.WriterRead.objects.all()
    serializer_class = serializers.WriterReadSerializer

class SettingViewSet(viewsets.ModelViewSet):
    queryset = WriterModel.Setting.objects.all()
    serializer_class = serializers.SettingSerializer

class SettingValueViewSet(viewsets.ModelViewSet):
    queryset = WriterModel.SettingValue.objects.all()
    serializer_class = serializers.SettingValueSerializer

class UserSettingsViewSet(viewsets.ModelViewSet):
    queryset = WriterModel.UserSettings.objects.all()
    serializer_class = serializers.UserSettingsSerializer

class FriendsViewSet(viewsets.ModelViewSet):
    queryset = PeopleModel.Friends.objects.all()
    serializer_class = serializers.FriendsSerializer

class FriendsRequestsViewSet(viewsets.ModelViewSet):
    queryset = PeopleModel.FriendsRequests.objects.all()
    serializer_class = serializers.FriendsRequestsSerializer

class MessagesViewSet(viewsets.ModelViewSet):
    queryset = MessageModel.Messages.objects.all()
    serializer_class = serializers.MessagesSerializer