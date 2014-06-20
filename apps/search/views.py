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
            
            try:
                page = request.POST.get('page')
                if page is None: page = 1
                page = int(page)
            except ValueError:
                page = 1


            searcher = get_searcher()
            results = searcher.search_page(query_parsed, page, 10)
            hits = len(results)
            
            pages = results.pagecount
            current_page = page
            has_previous = current_page > 1
            has_next = current_page < pages
            previous_page = current_page - 1 if has_previous else None
            next_page = current_page + 1 if has_next else None
            
            paginator = {
                    "pages" : pages,
                    "current_page" : current_page,
                    "has_previous" : has_previous,
                    "has_next" : has_next,
                    "previous_page" : previous_page,
                    "next_page" : next_page,
                }
            
            
            data = {
                    'hits' : hits,
                    'query' : query,
                    'results': results,
                    }
            data.update(paginator)
            
            return render(request, 'search/results.html', data)
    
        return redirect(reverse('search:search'))

class StorylineView(View):

    def get(self, request, *args, **kwargs):
        
        data = {'a' : kwargs.get('id')}
        
        return render(request, 'search/storyline.html', data)
