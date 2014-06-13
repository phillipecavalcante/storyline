from django.conf.urls import patterns, url

from apps.survey.views import SignupView, SigninView, StorylinesView, ActivateView, TicketView

urlpatterns = patterns('',
    url(r'^ticket$', TicketView.as_view(), name='ticket'),
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^signin$', SigninView.as_view(), name='signin'),
    url(r'^activate$', ActivateView.as_view(), name='activate'),
    url(r'^storylines$', StorylinesView.as_view(), name='storylines'),
)