import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from pprint import pprint
from utilities import *


class Dictionary():
    def __init__(self):
        self.dict = {
            'unaltered': set(),
            'altered': set(),
            'stopwords_removed': set(),
            'stemmed': set(),
            'normalized': set()
        }

    def make_dictionary(self):
        with open('corpus.json') as corpus:
            data = json.load(corpus)

            for entry in data:
                tokenized_fulltext = [lowercase_folding(word)
                                      for word in word_tokenize(entry['fulltext'])]

                self.dict['unaltered'] |= set(tokenized_fulltext)

                self.dict['altered'] |= normalize(stem(remove_stopwords(
                    tokenized_fulltext)))

        with open('dictionary.json', 'w') as outfile:
            uo_dict_lists = {k: list(v) for (k, v) in self.dict.items()}
            json.dump(uo_dict_lists, outfile, ensure_ascii=False, indent=4)
