import json
import re
from collections import defaultdict
from utilities import lowercase_folding


class InvertedIndex():
    def __init__(self):
        with open('corpus.json') as corpus:
            self.corpus = json.load(corpus)

        with open('dictionary.json') as dictionary:
            self.dictionary = json.load(dictionary)

    def make_inverted_index(self):
        inv_index = {key: defaultdict(list)
                     for key, _ in self.dictionary.items()}

        for key, wordlist in self.dictionary.items():
            inv_index[key] = self.fill_inv_index(wordlist)

        return inv_index

    def fill_inv_index(self, wordlist):
        inv_index_portion = defaultdict(list)

        for word in wordlist:
            for document in self.corpus:
                if contains_word(document['fulltext'], word) or contains_word(document['title'], word):
                    count = sum(1 for _ in re.finditer(r'\b%s\b' %
                                                       re.escape(lowercase_folding(word)), lowercase_folding(document['fulltext']))) + sum(1 for _ in re.finditer(r'\b%s\b' %
                                                                                                                                                                  re.escape(lowercase_folding(word)), lowercase_folding(document['title'])))
                    appearance = Appearence(document['doc_id'], count)
                    inv_index_portion[word].append(appearance)
        return inv_index_portion


def contains_word(fulltext, word):
    return re.compile(r'\b({0})\b'.format(re.escape(lowercase_folding(word))), flags=re.IGNORECASE).search(lowercase_folding(fulltext))


class Appearence():
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __contains__(self, key):
        return key == self.doc_id

    def __repr__(self):
        return str(self.__dict__)
