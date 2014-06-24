# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
#from django.core.urlresolvers import reverse

from apps.search.forms import SearchForm
from apps.search.models import Topic, Article
from apps.engine.query import parse
from apps.engine.searcher import get_searcher
from apps.engine.index import get_index
from whoosh import sorting
from apps.engine.chaining import lineup, storyline
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
                    'results': results
                    }
            data.update(paginator)
            
            return render(request, 'search/results.html', data)
    
        return redirect(reverse('search:search'))

class StorylineView(View):

    def get(self, request, *args, **kwargs):
        
        doc_id = kwargs.get('id')
        
        results = storyline(doc_id)
        
        data = {
                'initial' : results[0],
                'line' : 'storyline',
                'meth' : 'rte',
                'results' : results,
                }
        
        return render(request, 'search/lineup.html', data)

class LineUpView(View):

    def get(self, request, *args, **kwargs):
        
        line = kwargs.get('line')
        meth = kwargs.get('meth')
        doc_id = kwargs.get('id')
        
        results = lineup(doc_id, line, meth)

        data = {
                'initial' : results[0],
                'line' : line,
                'meth' : meth,
                'results' : results,
                }

        return render(request, 'search/lineup.html', data)


class ArticleView(View):

    def post(self, request, *args, **kwargs):
        
        if request.is_ajax():
        
            data = {}
            
            try:
                doc = Article.objects.get(pk=request.POST.get('id'))
            except Article.DoesNotExist:
                doc = None
            else:
                data.update({'doc' : doc})
            
            return render(request, 'search/article.html', data)