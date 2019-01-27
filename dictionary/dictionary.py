import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from pprint import pprint


class Dictionary():
    def __init__(self):
        self.dict = {
            'unaltered': set(),
            'stopwords_removed': set(),
            'stemmed': set(),
            'normalized': set()
        }
        self.stop_words = set(stopwords.words('english')) | set(
            stopwords.words('french'))
        self.stemmer = PorterStemmer()

    def make_dictionary(self):
        with open('corpus.json') as corpus:
            data = json.load(corpus)

            for entry in data:
                tokenized_title = word_tokenize(entry['title'])
                tokenized_fulltext = word_tokenize(entry['fulltext'])

                self.dict['unaltered'] |= set(tokenized_title)
                self.dict['unaltered'] |= set(tokenized_fulltext)

                self.dict['stopwords_removed'] |= set(
                    [w.lower() for w in tokenized_title if not w in self.stop_words])
                self.dict['stopwords_removed'] |= set(
                    [w.lower() for w in tokenized_fulltext if not w in self.stop_words])

                self.dict['stemmed'] |= set(
                    [self.stemmer.stem(w).lower() for w in tokenized_title])
                self.dict['stemmed'] |= set(
                    [self.stemmer.stem(w).lower() for w in tokenized_fulltext])

                self.dict['normalized'] |= set(normalize(tokenized_title))
                self.dict['normalized'] |= set(normalize(tokenized_fulltext))


def normalize(text):
    return {word.translate(str.maketrans('', '', string.punctuation)).lower() for word in text}
