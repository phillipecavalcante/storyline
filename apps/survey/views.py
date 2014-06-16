# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from smtplib import SMTPException
from passlib.hash import sha512_crypt

from apps.survey.forms import SignupForm, SigninForm, EmailForm, TicketForm
from apps.survey.models import Profile, Ticket

from project import settings
from os.path import join

# Create your views here.

class TicketView(View):

    def get(self, request):
        
        data = {'form' : EmailForm()}
        
        return render(request, 'survey/ticket.html', data)
    
    def post(self, request):
        
        form = EmailForm(request.POST)
        data = {'form' : form}
        
        if form.is_valid():
            
            user_email = request.POST.get('email')

            # get or create ticket
            try:
            
                ticket = Ticket.objects.get(email=user_email)
            
            except Ticket.DoesNotExist:
            
                user_token = sha512_crypt.encrypt(user_email)

                try:
                
                    ticket = Ticket(email=user_email, token=user_token)
                
                except Exception:
                
                    msg = "Não foi possível gerar um ticket. Por favor, tente mais tarde."
                    messages.error(request, msg, extra_tags='danger')
                    
                    return render(request, 'survey:ticket', data)
                
                else:
                
                    # send mail
                    subject = "Storyline ticket"
                    message = open(join(settings.BASE_DIR,"ticket_message.txt")).read().replace("<token>", user_token)
                    
                    storyline_email = settings.EMAIL_HOST_USER
                    
                    if send_mail(subject, message, storyline_email, [user_email], fail_silently=True) == 0:
                    
                        msg = "Não foi possível enviar um e-mail para %s. Por favor, tente mais tarde." % str(user_email)
                        messages.error(request, msg, extra_tags='danger')
                        
                        return render(request, 'survey/ticket.html', data)
                    
                    else:
                    
                        ticket.save()
                        return redirect(reverse('survey:signup'))
                        
            else:
            
                msg = "Um ticket já foi enviado para %s. Use outro e-mail." % str(user_email)
                messages.error(request, msg, extra_tags='danger')
                
                return redirect(reverse('survey:ticket'))
                
        else: # if form is invalid
        
            msg = "Ops! Verifique se algum campo do formulário não foi preenchido."
            messages.error(request, msg, extra_tags='danger')
            
            return render(request,'survey/ticket.html', data)

class SignupView(View):
    
    def get(self, request):

        data = {'form' : SignupForm()}

        return render(request, 'survey/signup.html', data)

    def post(self, request):
    
        form = SignupForm(request.POST)
        data = {'form' : form}
        
        if form.is_valid():
            
            
            user_email = request.POST.get('email')
            user_agreed = request.POST.get('agreed')
            user_passphrase = request.POST.get('passphrase')
            
            try:
            
                user_object = User.objects.create_user(
                                                    username=user_email,
                                                    email=user_email,
                                                    password=user_passphrase)
                user_object.is_active = False
                user_object.save()
            except IntegrityError:
                messages.error(request, "Email já cadastrado!", extra_tags='danger')
                return render(request, 'survey/signup.html', data)
            except Exception:
                messages.error(request, "Desculpe, não foi possível cadastrar o email %s. Tente outra vez." % str(user_email), extra_tags='danger')
                return render(request, 'survey/signup.html', data)
            
            else:
                try:
                    user_profile = Profile(user=user_object, agreed=user_agreed)
                except Exception:
                    messages.error(request, "Desculpe, tivemos um problema na criação do seu perfil de usuário com o email %s. Tente outra vez." % str(user_email), extra_tags='danger')
                    return render(request, 'survey/signup.html', data)
                else:
                    user_profile.save()
                    try:
                        activation_key = sha512_crypt.encrypt(user_object.password)
                        subject = """Storyline Confirmação de Email"""
                        message = """
                        Você está recebendo este email porque deseja participar do survey Storyline.\n
                        Copie a chave de ativação a seguir para ativar a sua conta de participação no survey Storyline:
                        <chave>\n
                        Se você não se cadastrou para participar do survey, por favor, despreze este email.
                        
                        Atenciosamente,
                        Phillipe Cavalcante
                        """.replace("<chave>", activation_key)
                        user_object.email_user(subject, message, from_email="noreply-storyline@outlook.com")
                    except SMTPSenderRefused:
                        messages.error(request, "Email inválido!", extra_tags='danger')
                        return render(request, 'survey/signup.html', data)
                    return redirect(reverse('survey:activate'))
        else:
            messages.error(request, "O formulário não foi preenchido corretamente.", extra_tags='danger')
            return render(request, 'survey/signup.html', data)

class SigninView(View):
    
    def get(self, request):
        data = {'form' : SigninForm()}
        return render(request, 'survey/signin.html', data)

    def post(self, request):

        form = SigninForm(request.POST)
        data = {'form' : form}

        if form.is_valid():
        
            user_email = request.POST.get('email')
            user_passphrase = request.POST.get('passphrase')
        
            user = authenticate(username=user_email, password=user_passphrase)
        
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('survey:storylines'))
                else:
                    messages.error(request, "Insira a chave de ativação que foi enviada para %s para ativar a sua conta." % str(user_email), extra_tags='danger')
                    return redirect(reverse('survey:activate'))
            else:
                messages.error(request, "Usuário não existe. Cadastre-se antes de fazer o login.", extra_tags='danger')
                return render(request, 'survey/signin.html', data)
        else:
            messages.error(request, "O formulário não foi preenchido corretamente.", extra_tags='danger')
            return render(request, 'survey/signin.html', data)

#class ActivateView(View):
#    
#    def get(self, request):
#        data = {'form' : ActivateForm()}
#        return render(request, 'survey/activate.html', data)
#
#    def post(self, request):
#        
#        form = ActivateForm(request.POST)
#        data = {'form' : form}
#
#        if form.is_valid():
#            
#            user_email = request.POST.get('email')
#            user_activation_key = request.POST.get('activation_key')
#            
#            try:
#                user = User.objects.get(email=user_email)
#            except User.DoesNotExist:
#                messsages.error(request, "Email não cadastrado.")
#                return render(request, 'survey/activate.html', data)
#            else:
#                if sha512_crypt.verify(str(user.password), str(user_activation_key)):
#                    user.is_active = True
#                    user.save()
#                    return redirect(reverse('survey:signin'))
#                else:
#                    messages.error(request, "Chave de ativação inválida.", extra_tags='danger')
#                    return render(request, 'survey/activate.html', data)
#    
#        else:
#            messages.error(request, "Formulário mal preenchido.", extra_tags='danger')
#            return render(request, 'survey/activate.html', data)

class StorylinesView(View):
    
    @login_required
    def get(self, request):
        return render(request, 'survey/storylines.html')
    