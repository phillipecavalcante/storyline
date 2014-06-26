# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.db import IntegrityError

from passlib.hash import sha512_crypt

from apps.survey.forms import SignUpForm, SignInForm, TicketForm
from apps.survey.models import *
from apps.search.models import *
from project import settings
from apps.engine.chaining import lineup

import os

# Create your views here.

MSG_FORM_INVALID = "Ops! Verifique se algum campo do formulário não foi preenchido."

class TicketView(View):
    """
    Ticket View
    
    User requests a ticket to be able to sign up.
    """
    
    MSG_TICKET_EXCEPTION = "Não foi possível enviar o ticket agora. Por favor, tente mais tarde."
    
    def get(self, request):
        
        if request.user.is_authenticated():
            messages.info(request, "Você já entrou na conta de participação.")
            return redirect(reverse('survey:storylines'))
            
        data = {'form': TicketForm()}
        
        return render(request, 'survey/ticket.html', data)
    
    def post(self, request):
        
        # Get filled form data.
        form = TicketForm(request.POST)
        data = {'form': form}
        
        if form.is_valid():
            
            user_email = request.POST.get('email')

            # Get ticket related to user's e-mail.
            try:
            
                ticket = Ticket.objects.get(email=user_email)
            
            except Ticket.DoesNotExist:
            
                # Generate a new token.
                user_token = sha512_crypt.encrypt(user_email)
                
                # Create a new ticket.
                try:
                
                    ticket = Ticket(email=user_email, token=user_token)
                
                except Exception:
                
                    # Ticket has not generated for some reason.
                    messages.error(request, self.MSG_TICKET_EXCEPTION, extra_tags='danger')
                    
                    return render(request, 'survey:ticket', data)
                
                else:
                
                    #Ticket has been generated.
                    
                    # Send ticket's e-mail
                    
                    subject = "Storyline ticket"
                    
                    # Open ticket's file.
                    try:
                        
                        filepath = os.path.join(settings.BASE_DIR, "ticket.txt")
                        f = open(filepath)
                    
                    except Exception:
                    
                        # Ticket's message has not been read.
                        messages.error(request, self.MSG_TICKET_EXCEPTION, extra_tags='danger')
                        
                        return render(request, 'survey:ticket', data)
                    
                    else:
                    
                        message = f.read().replace("<token>", user_token)
                    
                    finally:
                    
                        f.close()
                    
                    try:
                    
                        storyline_email = settings.EMAIL_HOST_USER
                    
                    except Exception:
                    
                        # E-mail sender is not correct.
                        messages.error(request, self.MSG_TICKET_EXCEPTION, extra_tags='danger')
                        
                        return render(request, 'survey:ticket', data)
                        
                    try:
                    
                        send_mail(subject, message, storyline_email, [user_email], fail_silently=True)
                    
                    except Exception:
                        
                        # Something went wrong when sending the e-mail.
                        messages.error(request, self.MSG_TICKET_EXCEPTION, extra_tags='danger')
                        
                        return render(request, 'survey:ticket', data)
                    
                    else:
                    
                        msg = "Um ticket foi enviado para %s." % str(user_email)
                        messages.info(request, msg, extra_tags='info')
                        ticket.save()
                        
                        return redirect(reverse('survey:signup'))
                        
            else:
            
                msg = "Um ticket já foi enviado para %s. Por favor, use outro e-mail." % str(user_email)
                messages.error(request, msg, extra_tags='danger')
                
                return redirect(reverse('survey:ticket'))
                
        else:
        
            # Form is invalid.
            messages.error(request, MSG_FORM_INVALID, extra_tags='danger')
            
            return render(request,'survey/ticket.html', data)

class SignUpView(View):
    """
    Signup View
    
    User sign up to be able to sign in and get started with the survey.
    """
    
    MSG_SIGNUP_EXCEPTION = "Não foi possível criar a sua conta. Tente mais tarde."
    
    def get(self, request):


        if request.user.is_authenticated():
            messages.info(request, "Você já entrou na conta de participação.")
            return redirect(reverse('survey:storylines'))
        
        data = {'form' : SignUpForm()}

        return render(request, 'survey/signup.html', data)

    def post(self, request):
        
        form = SignUpForm(request.POST)
        data = {'form' : form}
        
        if form.is_valid():
            
            user_ticket = request.POST.get('ticket')
            user_email = request.POST.get('email')
            user_passphrase = request.POST.get('passphrase')
            user_agreed = request.POST.get('agreed')
            
            if not user_agreed:
                msg = "Não faz sentido criar uma conta de participação se você não concorda com os termos de participação."
                messages.error(request, msg, extra_tags='danger')
                return redirect(reverse('survey:signup'))
            
            # Get user's ticket
            try:
                
                ticket = Ticket(token=user_ticket)
            
            except Ticket.DoesNotExist:
                
                msg = "Ticket inválido!"
                messages.error(request, msg, extra_tags='danger')
                return render(request, 'survey/signup.html', data)
            
            try:
            
                user_object = User.objects.create_user(
                                                    username=user_email,
                                                    email=user_email,
                                                    password=user_passphrase)
            
            except IntegrityError:
            
                messages.error(request, "Email já cadastrado!", extra_tags='danger')
                
                return render(request, 'survey/signup.html', data)
            
            except Exception:
            
                messages.error(request, self.MSG_SIGNUP_EXCEPTION, extra_tags='danger')
                
                return render(request, 'survey/signup.html', data)
            
            else:
            
                try:
                
                    user_profile = Profile(user=user_object, agreed=user_agreed)
                
                except Exception:
                
                    messages.error(request, self.MSG_SIGNUP_EXCEPTION, extra_tags='danger')
                    
                    return render(request, 'survey/signup.html', data)
                
                else:
                
                    user_profile.save()
                    messages.info(request, "Conta de participação criada com sucesso!", extra_tags='info')
                    
                    return redirect(reverse('survey:signin'))
        else:
        
            messages.error(request, MSG_FORM_INVALID, extra_tags='danger')
            
            return render(request, 'survey/signup.html', data)

class SignInView(View):
    
    MSG_SIGNIN_EXCEPTION = "Não foi possível entrar com a sua conta. Tente mais tarde."
    
    def get(self, request):
    
        if request.user.is_authenticated():
            messages.info(request, "Você já entrou na conta de participação.")
            return redirect(reverse('survey:storylines'))
        
        data = {'form' : SignInForm()}
        
        return render(request, 'survey/signin.html', data)

    def post(self, request):

        form = SignInForm(request.POST)
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
                
                    messages.error(request, self.MSG_SIGNIN_EXCEPTION, extra_tags='danger')
                    
                    return render(request, 'survey/signin.html', data)
            else:
            
                messages.error(request, self.MSG_SIGNIN_EXCEPTION, extra_tags='danger')
                
                return render(request, 'survey/signin.html', data)
        else:
        
            messages.error(request, MSG_FORM_INVALID, extra_tags='danger')
            
            return render(request, 'survey/signin.html', data)


class SignOutView(View):
    
    def get(self, request):
    
        logout(request)
        
        return redirect(reverse('survey:terms'))

class StorylinesView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StorylinesView, self).dispatch(*args, **kwargs)
    
    def get(self, request):
        
        results = request.user.story_set.all()
        
        data = {'results': results}
        
        return render(request, 'survey/storylines.html', data)

class UserStoryView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserStoryView, self).dispatch(*args, **kwargs)

    def get(self, request, id):
        
        line = 'storyline'
        meth = 'rte'
        
        story = Story.objects.get(id=id)
        results = story.storyrank_set.all().order_by('rank')

        # SUGGESTIONS TO IMPROVE THE STORYLINE
        relevant_results = lineup(str(story.first.id), 'relevance', 'bm25f')
        relevant_ids = set([rr['id'] for rr in relevant_results])
        result_ids = set([str(r.article.id) for r in results])
        suggestion_ids = relevant_ids - result_ids
   
        suggestions = [Article.objects.get(pk=s_id) for s_id in suggestion_ids]

        
        
        data = {
                'initial' : results[0],
                'line' : line,
                'meth' : meth,
                'results' : results,
                'suggestions': suggestions
                }

        return render(request, 'survey/storyline.html', data)

    def post(self, request, id):
        
        storyid = request.POST.get('storyid')
        userstory_ids = request.POST.get('userstory').split(',')
        print storyid
        print userstory_ids
        story = Story.objects.get(id=storyid)

        userstory = UserStory.objects.get(user=request.user, story=story)
        try:
            usr = UserStoryRank.objects.filter(userstory=userstory)
        except:
            pass
        else:
            usr.delete()
        
        for r, art_id in enumerate(userstory_ids):
            art = Article.objects.get(pk=art_id)
            UserStoryRank.objects.create(userstory=userstory, article=art, rank=r)
        
        messages.success(request, "Storyline criada com sucesso!")
        return render(request, 'survey/storyline.html')



class TermsView(View):

    def get(self, request):
        return render(request, 'survey/terms.html')

    