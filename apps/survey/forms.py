from django import forms
from django.forms import widgets

from captcha.fields import ReCaptchaField

class SubscribeForm(forms.Form):

    email = forms.EmailField()
    agreed = forms.BooleanField()
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})
    
    email.widget.attrs['class'] = 'form-control text-center'
    email.widget.attrs['placeholder'] = 'seu_email@exemplo.com'