# coding=UTF-8

"""
Translator
==========

Tradutor EN-PT do corpus RTE.
"""

try:
    import goslate
    gs = goslate.Goslate()
except ImportError:
    print "Ocorreu um erro na importação da biblioteca de tradução."
    raise

def translate(text, target="pt", source="en"):
    """
    translate(text[, target="pt", source="en"])
    
    .. code-block:: python
        
        >>> from rte import translator
        >>> translator.translate("Computer science")
        u'Ci\xeancia da Computa\xe7\xe3o'
    
    :param text: Texto a ser traduzido.
    :type text: str
    :param target: Idioma de destino.
    :type target: str
    :param source: Idioma de origem.
    :type source: str
    :returns: unicode
    """
    text_translated = gs.translate(text, target, source)
    return text_translated