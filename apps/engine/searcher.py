# -*- coding: utf-8 -*-

"""
Searcher
========

Searcher obtém o buscador do índice de documentos.
"""

try:
    from engine.index import get_index
    INDEX = get_index()
except ImportError:
    print "Não foi possível importar o índice padrão."
    raise

def get_searcher(index=INDEX, score_by="RTE"):
    """
    get_searcher([index=INDEX, score_by="RTE"])
    
    Obtém o buscador para o índice fornecido no parâmetro ``index``.
    O parâmetro ``score_by`` permite a escolha de uma função de pontuação diferente
    para o par (query, documento). As funções de pontuação disponíveis são:
    RTE, TFIDF e BM25F.
     
    .. code-block:: python
    
        >>> from searcher import get_searcher
        >>> from index import get_index
        >>>
        >>> idx = get_index()
        >>> searcher = get_searcher(idx, score_by="RTE")
        >>>
        
    :param index: Índice de documentos.
    :type index: FileIndex
    :param score_by: Função de pontuação entre a *query* do usuário e um documento recuperado.
    :type score_by: str
    :returns: Searcher
    """
    
    try:
        from scoring import RTE, BM25F, TF_IDF
    except ImportError:
        print "Ocorreu um erro na importação da função de pontuação RTE."
    
    # Converte para MAIÚSCULO.    
    score_by = score_by.upper()
    # Escolha da função de pontuação.
    if score_by == "RTE":
        score_function = RTE()
    elif score_by == "TFIDF":
        score_function = TF_IDF()
    elif score_by == "BM25F":
        score_function = BM25F()
    
    return index.searcher(weighting=score_function)
