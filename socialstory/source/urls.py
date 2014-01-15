from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.unregister.views.index', name='index'),
    #url(r'^login_redirect/$', 'apps.unregister.views.index', name='index'),
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login' ),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^acc/', include('apps.unregister.urls')),
    url(r'^writer/', include('apps.writer.urls')),
    url(r'^stories/', include('apps.stories.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)