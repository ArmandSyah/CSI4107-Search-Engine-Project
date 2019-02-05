import json
import re
from collections import defaultdict


class InvertedIndex():
    def __init__(self):
        with open('corpus.json') as corpus:
            self.corpus = json.load(corpus)

        with open('dictionary.json') as dictionary:
            self.dictionary = json.load(dictionary)

    def make_inverted_index(self):
        inv_index = defaultdict(list)

        for word in self.dictionary['unaltered']:
            for document in self.corpus:
                if contains_word(document['fulltext'], word):
                    count = sum(1 for _ in re.finditer(r'\b%s\b' %
                                                       re.escape(word), document['fulltext']))
                    appearance = Appearence(document['doc_id'], count)
                    inv_index[word].append(appearance)

        import pprint
        pprint.pprint(inv_index)

        return inv_index


def contains_word(fulltext, word):
    return f' {word} ' in f' {fulltext} '


class Appearence():
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __contains__(self, key):
        return key == self.doc_id

    def __repr__(self):
        return str(self.__dict__)
