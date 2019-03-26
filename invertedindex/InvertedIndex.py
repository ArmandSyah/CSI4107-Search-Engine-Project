import json
import re
from collections import defaultdict
from utilities import lowercase_folding
from utilities import *


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

        with open('corpus-reuters.json') as corpus:
            self.corpus_reuters = json.load(corpus)

        with open('dictionary.json') as dictionary:
            self.dictionary = json.load(dictionary)

    def make_inverted_index(self):
        inv_index = defaultdict(list)

        for index, corpus in enumerate([self.corpus, self.corpus_reuters]):
            print(f"reading - corpus #{index}")
            for document in corpus:
                bag_of_words_unique = set(lowercase_folding(word)
                                          for word in tokenize_word(document['title']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != "")
                bag_of_words_unique |= set(lowercase_folding(word)
                                           for word in tokenize_word(document['fulltext']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != "")
                for word in bag_of_words_unique:
                    if contains_word(document['fulltext'], word) or contains_word(document['title'], word):
                        count = sum(1 for _ in re.finditer(r'\b%s\b' %
                                                           re.escape(lowercase_folding(word)), lowercase_folding(document['fulltext']))) + sum(1 for _ in re.finditer(r'\b%s\b' %
                                                                                                                                                                      re.escape(lowercase_folding(word)), lowercase_folding(document['title'])))
                        appearance = Appearence(document['doc_id'], count)
                        inv_index[word].append(json.dumps(appearance.__dict__))

        with open('inverted_index.json', 'w') as outfile:
            json.dump(inv_index, outfile, ensure_ascii=False, indent=4)
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
            for index, corpus in enumerate([self.corpus, self.corpus_reuters]):
                print(f"reading - corpus #{index}")
                for document in corpus:
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
    return word in fulltext


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
