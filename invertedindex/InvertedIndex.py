import json
import re
from collections import defaultdict
from utilities import lowercase_folding


class InvertedIndex():
    """
        Handles building out the inverted index
        Loads both the corpus and dictionary json files and builds out the inverted index

        Inverted Index is structured as followed

        Inverted_Index = {
            'fully_altered': {
                "example word": [List of Appearance objects],
                ...
            }, ...
        }

        Since there were 5 different modes in the dictionary, the there are 5 different versions of the inverted index built 
        with the modes in mind (Ex: Inverted index for fully_altered dictionary words, ect.)
    """

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
        """
            Sets up the inverted index portion for a single dictionary mode
            Output looks as follows

            {
                "example word": [List of Appearance objects],
                ...
            }

            To count the words in the fulltext and title, used a regex to find every instance of the word, and sum them together

            The counting code was modified from https://stackoverflow.com/questions/17268958/finding-occurrences-of-a-word-in-a-string-in-python-3, from Amber's stack overflow answer
        """
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
    """
        Regex to find if word is in the fulltext

        This regex was modified from https://stackoverflow.com/questions/5319922/python-check-if-word-is-in-a-string, from Hugh Bothwell's stack overflow answer
    """
    return re.compile(r'\b({0})\b'.format(re.escape(lowercase_folding(word))), flags=re.IGNORECASE).search(lowercase_folding(fulltext))


class Appearence():
    """
    Represents a words appearance within the doc
    """

    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __contains__(self, key):
        return key == self.doc_id

    def __repr__(self):
        return str(self.__dict__)
