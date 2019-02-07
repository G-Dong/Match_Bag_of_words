from django.shortcuts import render
import sys
sys.path.append('C:/Users/kenwa/Desktop/cpm_demo/final/mysite/core')
from gensim import corpora, models, similarities
from core import util
import logging
import spacy
import string
import re
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import numpy as np
# Create your views here.
class Build_Corpora(object):
    def __init__(self):
        self.documents = list()
        self.texts = list()

    def add(self, source):
        self.documents.append(str(source))
        return self.documents

    def word_filter(self, string):
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
        stop_list = set('for a of the and to in is with'.split())
        self.texts = [[word for word in self.documents.lower().split()]
                      for self.documents in self.documents]
        # remove words that appear only once
        #pprint(self.texts)
        return self.texts

    def remove_once_words(self):
        from collections import defaultdict
        frequency = defaultdict(int)
        for text in self.texts:
            for token in text:
                frequency[token] += 1
        self.texts = [[token for token in text if frequency[token] > 1]
                      for text in self.texts]
        return self.texts

    def dictionary(self, path):
        dictionary = corpora.Dictionary(self.texts)
        dictionary.save(path)
        return dictionary

    def corpus(self, path, dictionary):
        corpus = [dictionary.doc2bow(text) for text in self.texts]
        corpora.MmCorpus.serialize(path, corpus)  # store to disk, for later use
        return corpus

    def save_dictionary(self, path):
        pass


def clean_text(text):
    ## Remove puncuation
    text = text.translate(string.punctuation)

    ## Convert words to lower case and split them
    text = text.lower().split()

    ## Remove stop words
    stops = set(stopwords.words("english"))
    text = [w for w in text if not w in stops and len(w) >= 3]

    text = " ".join(text)
    ## Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    ## Stemming
    text = text.split()
    stemmer = SnowballStemmer('english')
    stemmed_words = [stemmer.stem(word) for word in text]
    text = " ".join(stemmed_words)
    return text