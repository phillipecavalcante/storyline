# coding=UTF-8

"""
Translate Corpus
================

Script para tradução do corpus rte.
"""
from xmldoc import get_xml, translate_xml, create_xml
import pasta

def translate_corpus(root, append_name="_pt", target="pt", source="en"):
    """
    translate_corpus(root[, append_name="_pt", target="pt", source="en"])
    
    Cria um corpus traduzido do idioma ``source`` para o idioma ``target`` e 
    o retorna. O nome dos arquivos traduzidos e o diretório recebem um nome em
    anexo para diferenciá-los dos originais. Por exemplo, por padrão, se o nome
    do diretório for ``corpus``, o nome do diretório traduzido será ``corpus_pt``.
    Se o nome do arquivo for ``rte1_dev.xml``, o arquivo traduzido será
    ``rte1_dev_pt.xml``.
    Se o corpus traduzido já existe, retorna o corpus.
    
    :param corpus: Corpus RTE
    :type corpus: RTECorpusReader
    :param target: Idioma de destino
    :type target: str 
    :param source: Idioma de origem
    :type source: str
    :returns: RTECorpusReader
    """ 
    
    f = pasta.FilePath(root)
    source_xml_tree = get_xml(f.path)
    target_xml_tree = translate_xml(source_xml_tree)
    new_path = f.dir_path + append_name
    create_xml(target_xml_tree, pasta.join(new_path, f.fullname))
         

if __name__ == "__main__":
    
    
    root = "/Users/phillipe/Projects/storyline/apps/rte/corpus"
    _dir = pasta.DirPath(root)
    
    
    # Diretório não existe, criar.
    new_dirname = _dir.name + "_pt"
    _dir.create_beside(new_dirname)
    
    files = _dir.filter(exts=["xml"])
    for f in files:
        translate_corpus(f.path)