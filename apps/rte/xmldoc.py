# coding=UTF-8

"""
Xmldoc
======

Módulo de processamentos de arquivos XML com corpora de pares T-H para RTE.
"""

import xml.etree.ElementTree as ET
from translator import translate
import time
from xml.etree.ElementTree import ElementTree


def get_xml(filename):
    """
    get_xml(filename)
    
    :param filename: Nome completo do arquivo xml.
    :type filename: str
    :returns: ElementTree
    """
    tree = ET.parse(filename)
    return tree

def translate_xml(tree, target="pt", source="en", wait_line=0.5):
    """
    translate_etree(tree[target="pt", source="en", wait_line=0.5])
    
    Verte uma xml tree do idioma ``source`` para o idioma ``target``.
    O tempo padrão de espera entre uma tradução e outra é de 0.5 segundos.
    Se a quantidade de pares a traduzir for maior que 10 o tempo de espera
    é reconfigurado para 30s. Essa medida tenta evitar o encerramento da
    conexão com o google translate, mas não garante isso. #FIXME
    
    :param tree: Tree do XML.
    :type tree: ElementTree
    :param target: Idioma de destino
    :type target: str 
    :param source: Idioma de origem
    :type source: str
    :param wait_line: Tempo de espera de tradução entre linhas.
    :type wait_line: float
    :returns: ElementTree
    """
    CRITICAL_SIZE = 10 # seconds
    CRITICAL_WAIT_LINE = 1 # seconds
    # ROOT MUST BE COPIED!!!
    entailment_corpus = tree.getroot().copy()
    
    pairs = entailment_corpus.getchildren()
    
    pairs_size = len(pairs)
    if pairs_size > CRITICAL_SIZE and wait_line < CRITICAL_WAIT_LINE:
        print "Muitos pares rte na lista de tradução."
        print "O tempo de espera mínimo de tradução foi ajustado para %ds." % CRITICAL_WAIT_LINE
        wait_line = CRITICAL_WAIT_LINE # 30s
    
    count = 1 # Iniciando contagem
    for pair in pairs:
        print "Traduzindo par %d de %d" % (count, pairs_size)  
        pair.find("t").text = translate(pair.find("t").text, target, source)
        time.sleep(wait_line)
        pair.find("h").text = translate(pair.find("h").text, target, source)
        time.sleep(wait_line)
        count += 1
        
    translated_tree = ElementTree(entailment_corpus)
    
    return translated_tree
    
def create_xml(tree, filename):
    """
    create_xml(tree, filename)
    
    :param tree: XML tree
    :type tree: ElementTree
    :param filename: Nome completo do arquivo xml.
    :type filename: str
    """
    
    tree.write(filename)