# -*- coding: utf-8 -*-

"""
Index
=====

Index constrói índices de documentos com base num esquema que defina
a sua estrutura.

"""

try:
    
    from schema import get_schema
    SCHEMA = get_schema()
    
except ImportError:
    print "Ocorreu um erro ao importar o SCHEMA padrão."
    raise

try:
    
    import os
    from whoosh import index
    
except ImportError:
    print "Ocorreu um erro ao importar a biblioteca Whoosh."
    raise

try:
    from constants import INDEXDIR, INDEXNAME
except ImportError:
    print "Ocorreu um erro ao importar o módulo constants."
    raise

def index_exists(dirname=INDEXDIR, indexname=INDEXNAME):
    """
    index_exists([dirname="index", indexname="MAIN"])
    
    Verifica se o índice :attr:`indexname` existe no diretório :attr:`dirname`.
    
    .. code-block:: python
    
        from storyline.engine.index import index_exists
        
        # Exemplo em que existe o diretório index com índice MAIN.
        >>> index_exists() 
        True
        >>> index_exists("index")
        True
        >>> index_exists("index", "indexname")
        False
        
    :param dirname: Nome do diretório do índice.
    :type dirname: str
    :param indexname: Nome do índice.
    :tyoe indexname: str
    :returns: True ou False.
    """
    return index.exists_in(dirname, indexname.upper())

def get_index(dirname=INDEXDIR, indexname=INDEXNAME):
    """
    get([dirname="index", indexname="MAIN"])
    
    Obtém o índice :attr:`indexname` do diretório :attr:`dirname`, se existir.
    
    .. code-block:: python
    
        from storyline.engine.index import get_index
        
        >>> idx = get_index()
        >>> idx.indexname
        'MAIN'
        >>>
        >>> idx1 = get_index("index")
        >>> idx1.indexname
        'MAIN'
        >>>
        >>> idx2 = get_index("index", "indexname")
        >>> idx2.indexname
        ---------------------------------------------------------------------------
        AttributeError                            Traceback (most recent call last)
        ----> 1 idx2.indexname
        AttributeError: 'NoneType' object has no attribute 'indexname'
        >>> type(idx2)
        NoneType
        
        
    :param dirname: Nome do diretório do índice.
    :type dirname: str
    :param indexname: Nome do índice.
    :type indexname: str
    :returns: FileIndex  
    """
    # Assume que o índice não existe
    idx = None
    if index_exists(dirname, indexname): # Se existir
        idx = index.open_dir(dirname, indexname.upper())
    
    return idx
    
def build_index(schema=SCHEMA, dirname=INDEXDIR, indexname=INDEXNAME):
    """
    build_index([schema=SCHEMA, dirname="index", indexname="MAIN"])
    
    Constrói e retorna o índice com base no schema, se *não* existir.
    Se já existir, retorna o índice. 
    
    .. code-block:: python
    
        from storyline.engine.index import build_index
        from storyline.engine.schema import get_schema
        
        >>> SCHEMA = get_schema()
        >>> # constrói o índice
        >>> idx = build_index(SCHEMA) 
        >>> idx
        FileIndex(FileStorage('index'), 'MAIN')
        >>> 
        >>> idx1 = build_index(SCHEMA, "index", "indexname")
        >>> idx1
        FileIndex(FileStorage('index'), 'indexname')
        
        
    :param schema: Esquema do índice.
    :type schema: Schema  
    :param dirname: Nome do diretório do índice.
    :type dirname: str
    :param indexname: Nome do índice.
    :type indexname: str
    :returns: FileIndex 
    """
    # Verifica se o índice existe
    idx = get_index(dirname, indexname)
    if idx: return idx # retorna o índice
    
    # Cria o diretório do índice
    os.mkdir(dirname)
    # Cria e retorna o índice
    return index.create_in(dirname, schema, indexname.upper())