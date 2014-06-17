from django.conf.urls import patterns, url

from apps.survey.views import SignupView, SigninView, StorylinesView, TicketView, TermsView

urlpatterns = patterns('',
    url(r'^ticket$', TicketView.as_view(), name='ticket'),
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^signin$', SigninView.as_view(), name='signin'),
    url(r'^storylines$', StorylinesView.as_view(), name='storylines'),
    url(r'^terms$', TermsView.as_view(), name='terms'),
)