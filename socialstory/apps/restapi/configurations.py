from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'writers', views.WriterViewSet)
router.register(r'stories', views.StoriesViewSet)