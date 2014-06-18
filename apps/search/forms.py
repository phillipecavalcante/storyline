# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets


class SearchForm(forms.Form):

    search = forms.CharField()

    search.widget.attrs['class'] = 'form-control'