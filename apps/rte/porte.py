# coding=UTF-8

"""
PORTE
=====
"""

import nltk
from nltk.corpus.reader.rte import RTECorpusReader, RTEPair
import xml.etree.ElementTree as ET
import pasta
import pickle
from nltk.classify.rte_classify import ne
from whoosh import lang
from apps.engine.schema import analyze

class PORTEFeatureExtractor(object):
    """
    PORTEFeatureExtractor
    
    Esta classe é uma cópia da classe RTEFeatureExtractor exceto pela alteração
    dos valores dos atributos ``stopwords`` e ``negwords``, que foram substituídos
    pelos correspondentes valores em *Português*. Essa solução foi escolhida pelo
    dos atributos estarem acoplados a classe fortemente, dificultando a mudança
    para valores do idioma *Português*.
    
    Sendo assim, os comentários dos métodos pertencentes a esta classe foram
    omitidos, uma vez que o usuário pode consultar a classe original :class:`nltk.classify.rte_classify.RTEFeatureExtractor`. 
    """
    def __init__(self, rtepair, stop=True, lemmatize=False):
        
        self.stop = stop
        self.stopwords = lang.stopwords_for_language("pt")

        self.negwords = set(['não', 'nunca', 'falhou' 'rejeitou', 'negou', 'sem', 'jamais', 'nada', 'nenhum', 'nem', 'ninguém', 'menos', 'pouco'])
        # Try to tokenize so that abbreviations like U.S.and monetary amounts
        # like "$23.00" are kept as tokens.
        from nltk.tokenize import RegexpTokenizer
        tokenizer = RegexpTokenizer('([A-Z]\.)+|\w+|\$[\d\.]+')

        #Get the set of word types for text and hypothesis
        self.text_tokens = tokenizer.tokenize(rtepair.text)
        self.hyp_tokens = tokenizer.tokenize(rtepair.hyp)
        self.text_words = set(self.text_tokens)
        self.hyp_words = set(self.hyp_tokens)

        if lemmatize:
            self.text_words = set([lemmatize(token) for token in self.text_tokens])
            self.hyp_words = set([lemmatize(token) for token in self.hyp_tokens])

        if self.stop:
            self.text_words = self.text_words - self.stopwords
            self.hyp_words = self.hyp_words - self.stopwords

        self._overlap = self.hyp_words & self.text_words
        self._hyp_extra = self.hyp_words - self.text_words
        self._txt_extra = self.text_words - self.hyp_words


    def overlap(self, toktype, debug=False):
      
        ne_overlap = set([token for token in self._overlap if ne(token)])
        if toktype == 'ne':
            if debug: print "ne overlap", ne_overlap
            return ne_overlap
        elif toktype == 'word':
            if debug: print "word overlap", self._overlap - ne_overlap
            return self._overlap - ne_overlap
        else:
            raise ValueError("Type not recognized:'%s'" % toktype)

    def hyp_extra(self, toktype, debug=True):
        
        ne_extra = set([token for token in self._hyp_extra if ne(token)])
        if toktype == 'ne':
            return ne_extra
        elif toktype == 'word':
            return self._hyp_extra - ne_extra
        else:
            raise ValueError("Type not recognized: '%s'" % toktype)

def rte_features(rtepair):
    extractor = PORTEFeatureExtractor(rtepair)
    features = {}
    features['word_overlap'] = len(extractor.overlap('word'))
    features['word_hyp_extra'] = len(extractor.hyp_extra('word'))
    features['ne_overlap'] = len(extractor.overlap('ne'))
    features['ne_hyp_extra'] = len(extractor.hyp_extra('ne'))
    return features

class PORTE:
    """
    PORTE
    
    Container do classificador RTE.
    """
    def __init__(self, classifier=None):
        
        if classifier is None:
            filepath = "/Users/phillipe/Projects/storyline/apps/rte/classifier.pkl"
            self.classifier = get_classifier(filepath, mode="rb")
        else:
            self.classifier = classifier

    def rte(self, text, hyp):
        """
        rte(text, hyp)
        
        :param text: Texto-base do par.
        :type text: str
        :param hyp: Hipótese do par.
        :type hyp: str
        :returns: True ou False
        """

        rtepair = PORTEPair(text, hyp)
        return self.classifier.classify(rte_features(rtepair))

class PORTEPair:
    """
    PORTEPair
    
    Container para o par texto-hipótese.
    """
    
    def __init__(self, text, hyp):
        self.text = text
        self.hyp = hyp
    
        self.xmlpair = self.xml()
        self.rtepair = self.rtepair()
        
    def xml(self):
        """
        xml
        
        Transforma o par texto-hipótese para um par xml.
        
        :returns: xml.etree.ElementTree.Element
        """
        xmlpair = ET.Element("pair")
        xmlpair.attrib["id"] = "None"
        xmlpair.attrib["task"] = "entailment"
#         xmlpair.attrib["value"] = "None"
        t = ET.Element(self.text)
        h = ET.Element(self.hyp)
        xmlpair.append(t)
        xmlpair.append(h)
        return xmlpair
    
    def rtepair(self):
        """
        rtepair
        
        Obtém uma instância de RTEPair.
        
        :returns: instance of RTEPair
        """
        return RTEPair(self.xml())
        
class RTEClassifier:
    
    def __init__(self, root):
        self.__setup(root)
 
        self.train_set = [(rte_features(pair), pair.value) for pair in self.rte_reader_dev.pairs(self.fileids_dev)]
        self.test_set = [(rte_features(pair), pair.value) for pair in self.rte_reader_test.pairs(self.fileids_test)]

        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)
        
    def __setup(self, root):

        self.d = pasta.DirPath(root)
        self.fileids = [f.fullname for f in self.d.filter(exts=["xml"])]
        self.fileids_dev = [f.fullname for f in self.d.filter(exts=["xml"]) if f.name.endswith("dev")]
        self.fileids_test = [f.fullname for f in self.d.filter(exts=["xml"]) if f.name.endswith("test")]

        self.rte_reader_dev = RTECorpusReader(root, self.fileids_dev)
        self.rte_reader_test = RTECorpusReader(root, self.fileids_test)


    def get_accuracy(self):
        return nltk.classify.accuracy(self.classifier, self.test_set)
    
    def serialize(self, filename="classifier.pkl", mode="wb"):
 
        try:
            output = open(pasta.join(self.d.dir_path, filename), mode)
            pickle.dump(self.classifier, output)
        except IOError:
            print "Ocorreu um erro na serialização do classificador PORTE."
            raise

def get_classifier(filepath, mode="rb"):
    """
    get_classifier(filepath[, mode="rb"])
    
    Desserializa o classificador em modo de leitura binária.
    
    :param filepath: Caminho do arquivo pkl.
    :type filepath: str
    :param mode: Modo de leitura do arquivo pkl.
    :type mode: str
    :returns: nltk.classify.naivebayes.NaiveBayesClassifier
    """
    classifier_file = open(filepath, mode)
    classifier = pickle.load(classifier_file)
    
    return classifier

if __name__ == "__main__":
    pass