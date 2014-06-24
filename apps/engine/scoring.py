# -*- coding: utf-8 -*-
"""
Scoring
=======


"""

from searcher import get_searcher
from apps.rte.porte import PORTE
from schema import analyze

def score(text, hyp):

    # t  e h
    t = text['title']
    h = hyp['title']
    
    ana_t = analyze(t)
    ana_h = analyze(h)
    
    # INTER WORDS
    set_t = set(ana_t.split())
    set_h = set(ana_h.split())
    
    inter_score = len(set_t & set_h)
    
    # RTE
    porte = PORTE()
    rte_score = porte.rte(ana_t, ana_h)
    
    
    
    # DATE
    pubdate_score = 1 if text['pub_date'] <= hyp['pub_date'] else 0

    # LINKS
    links_score = 1 if text['url'] in  hyp['links'] else 0



    ## SCORE ##
    score = rte_score * 0.4 + pubdate_score * 0.1 + links_score * 0.3 + inter_score * 0.2
    
    return score
