from django.conf.urls import patterns, url

from apps.survey.views import SubscribeView

urlpatterns = patterns('',
    url(r'^subscribe$', SubscribeView.as_view(), name='subscribe'),
)