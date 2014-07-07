# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets

from captcha.fields import ReCaptchaField
from models import *

class SignUpForm(forms.Form):

    email = forms.EmailField()
    passphrase = forms.CharField(widget=forms.PasswordInput())
    agreed = forms.BooleanField()
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})
    ticket = forms.CharField()
    
    email.widget.attrs['class'] = 'form-control text-center'
    email.widget.attrs['placeholder'] = 'seu_email@exemplo.com'

    passphrase.widget.attrs['class'] = 'form-control text-center'
    passphrase.widget.attrs['placeholder'] = 'senha'
    
    ticket.widget.attrs['class'] = 'form-control text-center'
    ticket.widget.attrs['placeholder'] = 'ticket'
    
class SignInForm(forms.Form):

    email = forms.EmailField()
    passphrase = forms.CharField(widget=forms.PasswordInput())
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})
    
    email.widget.attrs['class'] = 'form-control text-center'
    email.widget.attrs['placeholder'] = 'seu_email@exemplo.com'

    passphrase.widget.attrs['class'] = 'form-control text-center'
    passphrase.widget.attrs['placeholder'] = 'senha'

class TicketForm(forms.Form):
    
    email = forms.EmailField()
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})
    
    email.widget.attrs['class'] = 'form-control text-center'
    email.widget.attrs['placeholder'] = 'seu_email@exemplo.com'


class ProfileForm(forms.Form):

    # profile
    age = forms.ChoiceField(choices=Profile.AGE_CHOICES, label="Faixa etária", required=False)
    edu = forms.ChoiceField(choices=Profile.EDU_CHOICES, label="Educação", required=False)
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, label="Gênero", required=False)

class EvalForm(forms.Form):
    # user story

    has_read = forms.ChoiceField(choices=UserStory.BOOLEAN_CHOICES, required=False,label="Já leu ou ouviu falar sobre este tópico antes?")
    has_context = forms.ChoiceField(choices=UserStory.BOOLEAN_CHOICES, required=False,label="De uma maneira geral, a storyline satisfaz a hipótese?")
    has_gap = forms.ChoiceField(choices=UserStory.BOOLEAN_CHOICES, required=False,label="Há a impressão de que falta alguma notícia na storyline?")
    has_similar = forms.ChoiceField(choices=UserStory.BOOLEAN_CHOICES, required=False,label="A storyline tem notícias similares?")