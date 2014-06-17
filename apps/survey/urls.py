from django.conf.urls import patterns, url

from apps.survey.views import SignUpView, SignInView, SignOutView, StorylinesView, TicketView, TermsView

urlpatterns = patterns('',
    url(r'^ticket$', TicketView.as_view(), name='ticket'),
    url(r'^signup$', SignUpView.as_view(), name='signup'),
    url(r'^signin$', SignInView.as_view(), name='signin'),
    url(r'^signout$', SignOutView.as_view(), name='signout'),
    url(r'^storylines$', StorylinesView.as_view(), name='storylines'),
    url(r'^terms$', TermsView.as_view(), name='terms'),
)