from django.shortcuts import render
from django.views.generic import View
# Create your views here.

class SubscribeView(View):

    def get(self, request):
        return render(request, 'survey/subscribe.html')