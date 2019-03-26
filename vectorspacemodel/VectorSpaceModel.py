import json
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
from utilities import *


class VectorSpaceModel():
    """
    Implementation of the Vector Space Retrieval Model
    For my implementation, tf is simply the raw frequencies of the word in the document
    Assume all words in the query have an equal weight, 1
    """

    def __init__(self, inv_index):
        with open('corpus.json') as corpus, open('corpus-reuters.json') as corpus_reuters:
            c = json.load(corpus)
            c_r = json.load(corpus_reuters)
            self.complete_set = {document['doc_id'] for document in c}
            self.complete_set |= {document['doc_id'] for document in c_r}
        self.inverted_index = inv_index
        self.mode = 'unaltered'

    def retrieve(self, query, mode):
        query = lowercase_folding(query)
        self.mode = mode

        if mode == 'fully_altered':
            query = normalize(stem(remove_stopwords(
                query)))
        elif mode == 'normalized':
            query = normalize(query)
        elif mode == 'stemmed':
            query = stem(query)
        elif mode == 'stopwords_removed':
            query = remove_stopwords(query)

        tokens = word_tokenize(query)
        query_vector = [1] * len(tokens)

        self.tf_idf_matrix = compute_tf_idf(
            self.complete_set,
            self.inverted_index[self.mode],
            compute_idf(self.complete_set, self.inverted_index[self.mode]))

        doc_vectors = compute_doc_vectors(
            self.complete_set, self.tf_idf_matrix, tokens)

        return compute_vector_scores(query_vector, doc_vectors)


def compute_idf(complete_set, inverted_index):
    """
    Get the inverted index for each word
    """
    number_of_docs = len(complete_set)
    return {word: math.log10(number_of_docs / len(docs))
            for word, docs in inverted_index.items()}


def compute_tf_idf(complete_set, inverted_index, idf_index):
    """
    Set up the TF-IDF matrix, indexed 2-dimensionally by word and then doc
    """
    tf_idf = defaultdict(lambda: defaultdict(int))
    for word, docs in inverted_index.items():
        placeholder = defaultdict(int)
        for doc_id in complete_set:
            placeholder[doc_id] = 0
        for appearance in docs:
            placeholder[appearance.doc_id] = appearance.frequency * \
                idf_index[word]
        tf_idf[word] = placeholder

    return tf_idf


def compute_doc_vectors(complete_set, tf_idf_matrix, tokens):
    """
        Retrieve the weight of each word from the query in the doc, from the tf_idf matrix, 
        store them in the following structure

        Example Query: "nice day outside"

        {
            "CSI-1": (<weight of word 'nice'>, <weight of word 'day'>, <weight of word 'outside'>),
            ...
        }


    """
    doc_vectors = defaultdict(tuple)

    for doc_id in complete_set:
        vector = []
        for token in tokens:
            set_of_docweights = tf_idf_matrix[token]
            weight = set_of_docweights[doc_id]
            vector.append(weight)
        doc_vectors[doc_id] = vector

    return doc_vectors


def compute_vector_scores(query_vector, doc_vectors):
    """
        Set up a list of scores for each document 
    """
    scores = []
    for doc_id, vector in doc_vectors.items():
        score = 0
        for query_vector_weight, doc_tf_idf in zip(query_vector, vector):
            score += query_vector_weight * doc_tf_idf
        scores.append((doc_id, score))
    scores.sort(key=lambda tup: tup[1], reverse=True)
    return [score for score in scores if score[1] != 0]
