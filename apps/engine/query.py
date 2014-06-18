# -*- coding: utf-8 -*-

"""
Query
=====

Query processa o texto do usuário para o formato do esquema do índice.

"""
try:
    from apps.engine.schema import get_schema
    SCHEMA = get_schema()
except ImportError:
    print "Ocorreu um erro ao importar o SCHEMA padrão."
    raise

def parse(text, schema=SCHEMA):
    """
    parse(text[, schema=SCHEMA])
    
    Analisa e trata o texto em ``text`` de acordo com o ``schema``
    do índice de documentos.
     
    .. code-block:: python
    
        >>> from storyline.engine.query import parse
        >>> from storyline.engine.schema import get_schema
        >>>
        >>> SCHEMA = get_schema()
        >>> parse("Mestre", SCHEMA)
        Or([Term('title', u'mestr'), Term('content', u'mestr')])
    
    :param text: Consulta feita pelo usuário.
    :type text: str
    :param schema: Schema do índice de documentos.
    :type schema: Schema
    :returns: Query com termos e operadores.
    """
    
    try:
        from whoosh.qparser import MultifieldParser
    except ImportError:
        print "Ocorreu um erro na importação do módulo whoosh.qparser."
        
    qp = MultifieldParser(["title", "content"], schema, None)
    
    return qp.parse(text)