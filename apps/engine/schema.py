# -*- coding: utf-8 -*-

"""
Schema 
======

Schema define os campos do índice de busca de documentos.

Este módulo é um container de esquemas.
Atualmente, este container armazena apenas um esquema para suporte ao índice
da classe :class:`apps.search.models.Article`.
Outros esquemas podem ser adicionados com base no método :meth:`get_schema`.

"""

try:
    
    from whoosh.fields import Schema, ID, TEXT, DATETIME
    from whoosh.analysis import LanguageAnalyzer
    from whoosh.lang import languages
    
except ImportError:
    print "Ocorreu um erro ao importar a biblioteca Whoosh."
    raise

def get_schema(lang=languages[10]):
    """
    get_schema([lang="pt"])
    
    Obtém o esquema a ser usado para a criação do índice de documentos.
    Por padrão, o esquema é carregado com o analisador de textos para o idioma
    Português. Mas, pode ser carregado para qualquer um dos idiomas suportados
    pela biblioteca Whoosh. Atualmente Whoosh suporta os seguintes idiomas:
    
    .. code-block:: python

        >>> from whoosh.lang import languages
        >>> languages
        ('ar', 'da', 'nl', 'en', 'fi', 'fr', 'de', 'hu', 'it', 'no',
        'pt', 'ro', 'ru', 'es', 'sv', 'tr')

    
    Os campos que compõem o índice de documentos não necessariamente precisam
    ser todos os campos que compõem o documento.
    
    Este esquema contém 4 campos - ``id``, ``pub_date``, ``title`` e
    ``body`` - dos 6 campos da classe :class:`apps.search.models.Article`,
    que define um documento neste projeto.
    
    O esquema do índice de documentos para a classe Article é o seguinte:
    
    .. code-block:: python
    
        Schema(
                id = ID(unique=True, stored=True),
                pub_date = DATETIME(stored=True),
                title = TEXT(stored=True,
                            analyzer=LanguageAnalyzer(lang)),
                body = TEXT(stored=True,
                               analyzer=LanguageAnalyzer(lang)),
               )
    
    Os campos ``title`` e ``body``, por serem de tipo ``TEXT``, podem receber
    processamento textual que varia de acordo com o idioma. O idioma padrão
    deste método é o Português. O parâmetro ``lang`` permite alterar o idioma
    para um dos idiomas listados em :mod:`whoosh.lang.languages`. 
    A escolha do idioma é importante para que a análise léxico-sintática sobre
    o texto seja feita corretamente.
    O analisador de textos :class:`LanguageAnalyzer` usa 3 filtros para
    o processamento textual nos campos ``title`` e ``body``:
    LowercaseFilter (converte para letras minúsculas),
    StopFilter (remove palavras irrelevantes) e
    StemFilter (converte para a raiz da palavra).
    
    Todos os campos do schema também são armazenados no índice de documentos.
    O parâmetro ``stored=True`` indica que os campos serão indexados e armazenados.
    O parâmetro ``unique`` informa que o campo é único. 
    
    :param lang: Idioma do Schema.
    :type lang: str
    
    :returns: Schema
    """
    return Schema(
                  id = ID(unique=True, stored=True),
                  pub_date = DATETIME(stored=True),
                  title = TEXT(stored=True,
                               analyzer=LanguageAnalyzer(lang)),
                  body = TEXT(stored=True,
                                 analyzer=LanguageAnalyzer(lang)),
                  )