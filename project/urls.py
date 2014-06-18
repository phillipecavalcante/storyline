from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'storyline.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.search.urls', namespace='search')),
    url(r'^survey/', include('apps.survey.urls', namespace='survey')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
