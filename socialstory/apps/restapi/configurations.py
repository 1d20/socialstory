from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'genre', views.GenreViewSet)
router.register(r'subgenre', views.SubGenreViewSet)
router.register(r'stories', views.StoriesViewSet)
router.register(r'language', views.LanguageViewSet)
router.register(r'similar_story', views.SimilarStoryViewSet)
router.register(r'versions', views.VersionsViewSet)
router.register(r'writer', views.WriterViewSet)
router.register(r'comment', views.CommentsViewSet)
router.register(r'writer_vote', views.WriterVoteViewSet)
router.register(r'writer_favorite', views.WriterFavoriteViewSet)
router.register(r'writer_read', views.WriterReadViewSet)
router.register(r'setting', views.SettingViewSet)
router.register(r'setting_value', views.SettingValueViewSet)
router.register(r'user_settings', views.UserSettingsViewSet)
router.register(r'friends', views.FriendsViewSet)
router.register(r'friends_requests', views.FriendsRequestsViewSet)
router.register(r'messages', views.MessagesViewSet)