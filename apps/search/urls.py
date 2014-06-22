from django.conf.urls import patterns, url

from apps.search.views import *

DOC  = '(?P<id>\d+)'
LINE = '(?P<line>(timeline|relevance))'
METH = '(?P<meth>(tfidf|bm25f))'
ART  = 'article'

SEARCH    = '^' + '$'
STORYLINE = '^' + DOC + '$'
LINEUP    = '^' + DOC + '/' + LINE + '/' + METH + '$'
ARTICLE   = '^' + ART + '/' + '$'

urlpatterns = patterns('',
    url(SEARCH   , SearchView.as_view()   , name='search'),
    url(STORYLINE, StorylineView.as_view(), name='storyline'),
    url(LINEUP   , LineUpView.as_view()   , name='lineup'),
    url(ARTICLE  , ArticleView.as_view()  , name='article'),
)