from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.restapi.configurations import router

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'apps.unregister.views.index', name='index'),

    url(r'^acc/', include('apps.unregister.urls')),
    url(r'^writer/', include('apps.writer.urls')),
    url(r'^stories/', include('apps.stories.urls')),
    url(r'^people/', include('apps.people.urls')),
    url(r'^message/', include('apps.messages.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
)

print settings.STATIC_URL, settings.STATIC_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)