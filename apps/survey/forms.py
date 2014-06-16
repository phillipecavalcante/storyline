# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets

from captcha.fields import ReCaptchaField

class SignupForm(forms.Form):

    email = forms.EmailField()
    passphrase = forms.CharField(widget=forms.PasswordInput())
    agreed = forms.BooleanField()
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})
    
    email.widget.attrs['class'] = 'form-control text-center'
    email.widget.attrs['placeholder'] = 'seu_email@exemplo.com'

    passphrase.widget.attrs['class'] = 'form-control text-center'
    passphrase.widget.attrs['placeholder'] = 'senha'
    
class SigninForm(forms.Form):

    email = forms.EmailField()
    passphrase = forms.CharField(widget=forms.PasswordInput())
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})
    
    email.widget.attrs['class'] = 'form-control text-center'
    email.widget.attrs['placeholder'] = 'seu_email@exemplo.com'

    passphrase.widget.attrs['class'] = 'form-control text-center'
    passphrase.widget.attrs['placeholder'] = 'senha'

#class ActivateForm(forms.Form):
#    
#    email = forms.EmailField()
#    activation_key = forms.CharField(widget=forms.PasswordInput())
#    
#    
#    email.widget.attrs['class'] = 'form-control text-center'
#    email.widget.attrs['placeholder'] = 'seu_email@exemplo.com'
#
#    activation_key.widget.attrs['class'] = 'form-control text-center'
#    activation_key.widget.attrs['placeholder'] = 'chave de ativação'

class EmailForm(forms.Form):
    
    email = forms.EmailField()
    
    email.widget.attrs['class'] = 'form-control text-center'
    email.widget.attrs['placeholder'] = 'seu_email@exemplo.com'

class TicketForm(forms.Form):
    
    email = forms.EmailField()
    ticket = forms.CharField(widget=forms.PasswordInput())
    
    
    email.widget.attrs['class'] = 'form-control text-center'
    email.widget.attrs['placeholder'] = 'seu_email@exemplo.com'

    ticket.widget.attrs['class'] = 'form-control text-center'
    ticket.widget.attrs['placeholder'] = 'chave de ativação'
