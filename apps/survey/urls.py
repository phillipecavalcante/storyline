from django.conf.urls import patterns, url

from apps.survey.views import *

urlpatterns = patterns('',
    url(r'^ticket$', TicketView.as_view(), name='ticket'),
    url(r'^signup$', SignUpView.as_view(), name='signup'),
    url(r'^signin$', SignInView.as_view(), name='signin'),
    url(r'^signout$', SignOutView.as_view(), name='signout'),
    url(r'^storylines$', StorylinesView.as_view(), name='storylines'),
    url(r'^storylines/(?P<id>\d+)$', UserStoryView.as_view(), name='userstory'),
    url(r'^storylines/(?P<id>\d+)/eval$', EvalStoryView.as_view(), name='evalstory'),
    url(r'^analysis$', AnalysisView.as_view(), name='analysis'),
    url(r'^terms$', TermsView.as_view(), name='terms'),
)