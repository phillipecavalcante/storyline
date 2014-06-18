# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from apps.search.forms import SearchForm
from apps.search.models import Topic, Article
from apps.engine.query import parse
from apps.engine.searcher import get_searcher

# Create your views here.

class SearchView(View):

    def get(self, request):
    
        data = {'form' : SearchForm()}
        
        try:
            topics = Topic.objects.all().order_by('name')
        except Exception:
            pass
        else:
            data.update({'topics': topics})
        
        
        return render(request, 'search/search.html', data)

    def post(self, request):

        if request.is_ajax():
        
            query = request.POST.get('query')
            
            query_parsed = parse(query)
            searcher = get_searcher()
            
            results = searcher.search(query_parsed)

            paginator = Paginator(results, 10)

            try:
                page = request.POST.get('page')
            except ValueError:
                page = 1

            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            data = {
                    'query' : query,
                    'results': results
                    }
            
            return render(request, 'search/results.html', data)