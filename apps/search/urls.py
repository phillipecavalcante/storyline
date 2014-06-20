from django.conf.urls import patterns, url

from apps.search.views import SearchView, StorylineView

DOC = r'^(?P<id>\d+)$'

urlpatterns = patterns('',
    url(r'^$', SearchView.as_view(), name='search'),
    url(DOC, StorylineView.as_view(), name='lineup'),
)