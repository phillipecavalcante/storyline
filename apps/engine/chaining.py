# -*- coding: utf-8 -*-

from query import parse
from searcher import get_searcher
from scoring import score
from query import parse
from schema import analyze

def implies(hyp, results):
    
    scoredresults = []
    
    for text in results:
        pair = (text, score(text, hyp))
        scoredresults.append(pair)
    
    sortedresults = sorted(scoredresults, key=lambda h:h[1], reverse=True)

    try:
        text = sortedresults[1][0]
    except IndexError:
        text = hyp

    return text

def storyline(doc_id):
    
    results = lineup(doc_id, top=30)

    hyp = results[0]
    
    max_docs = 10
    count = 0
    chaining = []
    
    while count < max_docs and not (hyp in chaining):
        chaining.append(hyp)
        count = count + 1
        text = implies(hyp, results)
        hyp = text

    return chaining

def lineup(doc_id, line='relevance', meth='bm25f', top=10):
    
    searcher = get_searcher(score_by=meth)
#    docnum = searcher.document_number(id=doc_id)
    initial = searcher.document(id=doc_id)
    
#    results = searcher.more_like(docnum, 'title', top=top)
    query = analyze(initial['title'])

    query_improved = u' '.join(query.strip().split()).replace(' ', ' OR ')

    query_parsed = parse(query_improved)
    
    #query_parsed = parse(query)
    results = searcher.search(query_parsed, limit=top)
    
    try:
        results = results[1:]
    except IndexError:
        results = None

    results = list(results)
    
    if line == 'timeline':
        results = sorted(results, key=lambda d: d['pub_date'], reverse=True)
    
    results.insert(0, initial)
        
    return results


