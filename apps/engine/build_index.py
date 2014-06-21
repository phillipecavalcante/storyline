# -*- coding: utf-8 -*-

"""
Build Index
===========

Script de construção do índice de documentos da classe
:class:`apps.search.models.Article`.

Procedimento do script:

#. Carrega os módulos index, schema e Article.
#. Contrói ou recupera o índice.
#. Lista os documentos a serem indexados.
#. Adiciona os documentos ao índice.

"""

def add_docs(documents, index):
    """
    add_docs(documents, index)
    
    Adiciona os documentos obtidos de :class:`apps.search.models.Article` ao 
    índice existente.
    
    .. code-block:: python
        
        from storyline.engine.index import get_index
        from apps.search.models import Article
        
        >>> idx = get_index()
        >>> docs = Article.objects.all()
        >>> add_docs(docs, idx)
    
    :param index: Índice de documentos.
    :type index: FileIndex
    :param documents: Lista de documentos.
    :type documents: list
    """
    writer = index.writer()
    for doc in documents:
        writer.add_document(
                            id = unicode(doc.id),
                            pub_date = doc.pub_date,
                            title = unicode(doc.title),
                            body = unicode(doc.body),
                            source = unicode(doc.source),
                            url = unicode(doc.url),
                            links = unicode(doc.links)
                            )
    writer.commit()

if __name__ == "__main__":
    
    try:
        print "Importando módulos..."
        import os, sys, index
        
        ## Adicionando ambiente Django
        print "Adicionando ambiente Django..."
        sys.path.insert(0, '/Users/phillipe/Projects/storyline')
        os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
        from apps.search.models import Article
    except ImportError:
        print "Ocorreu um erro na importação dos módulos necessários\
         para a construção do índice e inclusão dos documentos."
        raise
    
    # Criando índice
    try:
        print "O índice está sendo construído, ou obtido (se já existir)..."
        idx = index.build_index()
    except:
        print "Não foi possível obter o índice."
        raise
    
    
    try:
        print "Lendo os documentos a serem indexados..."
        docs = Article.objects.all()
    except Article.DoesNotExist:
        print "Não foi possível carregar a lista de documentos."
        raise
    
    try:
        print "Adicionando os documentos ao índice..."
        add_docs(docs, idx)
        print "Total de documentos indexados:", idx.doc_count()
    except:
        print "Ocorreu um problema na adição dos documentos ao índice."
        raise