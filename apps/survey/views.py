from django.shortcuts import render
from django.views.generic import View

from apps.survey.forms import SubscribeForm

# Create your views here.

class SubscribeView(View):
    
    def get(self, request):

        data = {'form' : SubscribeForm()}

        return render(request, 'survey/subscribe.html', data)

    def post(self, request):
    
        form = SubscribeForm(request.POST)
        data = {'form' : form}
        
        if form.is_valid():
            
            user_email = request.POST.get('email')
            user_agreed = request.POST.get('agreed')
            
            return render(request, 'survey/subscribe.html')
        else:
            return render(request, 'survey/subscribe.html', data)