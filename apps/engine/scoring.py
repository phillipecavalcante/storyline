# -*- coding: utf-8 -*-
"""
Scoring
=======


"""
import random

try:
    # BM25F e TF_IDF são usados no módulo searcher.py.
    from whoosh.scoring import BM25F, TF_IDF
except ImportError:
    print "Ocorreu um erro na importação do módulo scoring de Whoosh."
    raise

class RTE(TF_IDF):
    
    use_final=True
    
    def final(self, searcher, docnum, score):
        
        titulo = searcher.stored_fields(docnum).get("title")
        return random.random()