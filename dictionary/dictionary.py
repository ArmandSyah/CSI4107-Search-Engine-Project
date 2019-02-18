import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from utilities import *


class Dictionary():
    def __init__(self):
        self.dict = {
            'unaltered': set(),
            'fully_altered': set(),
            'stopwords_removed': set(),
            'stemmed': set(),
            'normalized': set()
        }

    def make_dictionary(self):
        with open('corpus.json') as corpus:
            data = json.load(corpus)

            for entry in data:
                tokenized_title = [lowercase_folding(word)
                                   for word in word_tokenize(entry['title']) if word not in string.punctuation]
                tokenized_fulltext = [lowercase_folding(word)
                                      for word in word_tokenize(entry['fulltext']) if word not in string.punctuation]

                self.dict['unaltered'] |= set(tokenized_title)
                self.dict['unaltered'] |= set(tokenized_fulltext)

                self.dict['fully_altered'] |= set(tokenized_title)
                self.dict['fully_altered'] |= normalize(stem(remove_stopwords(
                    tokenized_fulltext)))

                self.dict['stopwords_removed'] |= set(tokenized_title)
                self.dict['stopwords_removed'] |= remove_stopwords(
                    tokenized_fulltext)

                self.dict['stemmed'] |= set(tokenized_title)
                self.dict['stemmed'] |= stem(tokenized_fulltext)

                self.dict['normalized'] |= set(tokenized_title)
                self.dict['normalized'] |= normalize(tokenized_fulltext)

        with open('dictionary.json', 'w') as outfile:
            uo_dict_lists = {k: list(v) for (k, v) in self.dict.items()}
            json.dump(uo_dict_lists, outfile, ensure_ascii=False, indent=4)
