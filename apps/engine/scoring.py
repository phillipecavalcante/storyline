# -*- coding: utf-8 -*-
"""
Scoring
=======


"""

from searcher import get_searcher
from apps.rte.porte import PORTE

def score(text, hyp):

    # RTE
    porte = PORTE()
    rte_score = porte.rte(text['title'], hyp['title'])

    # DATE
    pubdate_score = 1 if text['pub_date'] <= hyp['pub_date'] else 0

    # LINKS
    links_score = 1 if text['url'] in  hyp['links'] else 0

    ## SCORE ##
    score = rte_score * 2 + pubdate_score + links_score * 3

    return score
