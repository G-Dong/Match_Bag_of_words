import sys
sys.path.append('C:/Users/kenwa/Desktop/cpm_demo/final/mysite/core')
from gensim import corpora, models, similarities
import logging
import spacy
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class BuildCorpora(object):
    """
    This method concludes several manipulations on cleaned Competency Moedel to build the NLP usable dictionary
    """
    def __init__(self):
        self.documents = list()
        self.texts = list()

    def add(self, source):
        """
        :param source: strings
        :return: appended documents
        """
        self.documents.append(str(source))
        return self.documents

    @staticmethod
    def word_filter(string):
        """
        :param string: input documents
        :return: documents only contains noun, propn, verbs and adj
        """
        nlp = spacy.load('en')
        doc = nlp(string)
        result = list()
        for i, token in enumerate(doc):
            if token.pos_ in ('NOUN', 'PROPN', 'VERB', 'ADJ'):
                #print(doc[i])
                result.append(doc[i])
        #print(result)
        return result

    # remove common words and tokenize
    def remove_stop_words(self):
        """
        :return: docuemnts without stop words
        """
        stop_list = set('for a of the and to in is with'.split())
        self.texts = [[word for word in self.documents.lower().split()]
                      for self.documents in self.documents]
        # remove words that appear only once
        #pprint(self.texts)
        return self.texts

    def remove_once_words(self):
        """
        :return: remove words which only exits once.
        """
        from collections import defaultdict
        frequency = defaultdict(int)
        for text in self.texts:
            for token in text:
                frequency[token] += 1
        self.texts = [[token for token in text if frequency[token] > 1]
                      for text in self.texts]
        return self.texts

    def dictionary(self, path):
        """
        :param path: the path which the dictionary should be saved
        :return: save operation and saved documents.
        """
        dictionary = corpora.Dictionary(self.texts)
        dictionary.save(path)
        return dictionary

    def corpus(self, path, dictionary):
        """
        :param path: the path which the corpus should be saved
        :param dictionary: the existing dictionary
        :return: save operation and saved corpus
        """
        corpus = [dictionary.doc2bow(text) for text in self.texts]
        corpora.MmCorpus.serialize(path, corpus)  # store to disk, for later use
        return corpus


    def add_synonym(self):
        """

        :return: return the synonym collections of words inside the traits
        """
        self.texts()

    def save_dictionary(self, path):
        pass