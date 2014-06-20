# -*- coding: utf-8 -*-
"""
Scoring
=======


"""

try:
    # BM25F e TF_IDF são usados no módulo searcher.py.
    from whoosh.scoring import BM25F, TF_IDF
    from apps.rte import porte
except ImportError:
    print "Ocorreu um erro na importação do módulo scoring de Whoosh."
    raise

class RTE(TF_IDF):
    
    use_final=True
    
    def final(self, searcher, docnum, score):
        
        text = searcher.stored_fields(docnum).get('title')
        hyp = searcher.document()['title']
        
        p = porte.PORTE()
        rte_value = p.rte(text, hyp)
        
        print rte_value

        return 1
