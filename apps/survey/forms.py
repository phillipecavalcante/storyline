from django import forms
from django.forms import widgets

class SubscribeForm(forms.Form):

    email = forms.EmailField(required=True)
