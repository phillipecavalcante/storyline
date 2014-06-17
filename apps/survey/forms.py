# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets

from captcha.fields import ReCaptchaField

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