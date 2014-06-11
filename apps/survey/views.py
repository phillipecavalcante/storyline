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
            return render(request, 'survey/subscribe.html')
        else:
            data.update({'x':'fasdfs'})
            return render(request, 'survey/subscribe.html', data)