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
            'altered': set(),
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

                self.dict['altered'] |= normalize(stem(remove_stopwords(
                    tokenized_title, self.stop_words), self.stemmer))
                self.dict['altered'] |= normalize(stem(remove_stopwords(
                    tokenized_fulltext, self.stop_words), self.stemmer))

        with open('dictionary.json', 'w') as outfile:
            uo_dict_lists = {k: list(v) for (k, v) in self.dict.items()}
            json.dump(uo_dict_lists, outfile, ensure_ascii=False, indent=4)


def normalize(text):
    return {word.translate(str.maketrans('', '', string.punctuation)).lower() for word in text}


def remove_stopwords(text, stop_words):
    return set([w.lower() for w in text if not w in stop_words])


def stem(text, stemmer):
    return set([stemmer.stem(w).lower() for w in text])
