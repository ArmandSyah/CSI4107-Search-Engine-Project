import json
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
from utilities import *

# tf uses raw frequencies
# assume all weights in each word of query have weight 1


class VectorSpaceModel():
    def __init__(self, inv_index):
        with open('corpus.json') as corpus:
            c = json.load(corpus)
            self.complete_set = {document['doc_id'] for document in c}
        self.inverted_index = inv_index
        self.tf_idf_matrix = compute_tf_idf(
            self.complete_set,
            inv_index,
            compute_idf(self.complete_set, inv_index))

    def retrieve(self, query):
        query = lowercase_folding(query)
        tokens = remove_stopwords(word_tokenize(query))
        query_vector = (1) * len(tokens)
        doc_vectors = compute_doc_vectors(
            self.complete_set, self.tf_idf_matrix, tokens)
        scores = compute_vector_scores(query_vector, doc_vectors)


def compute_idf(complete_set, inverted_index):
    number_of_docs = len(complete_set)
    return {word: math.log10(number_of_docs/len(docs))
            for word, docs in inverted_index.items()}


def compute_tf_idf(complete_set, inverted_index, idf_index):
    tf_idf = defaultdict(lambda: defaultdict(int))
    for word, docs in inverted_index.items():
        placeholder = defaultdict(int)
        for appearance in docs:
            placeholder[appearance.doc_id] = appearance.frequency * \
                idf_index[word]
        tf_idf[word] = placeholder
    return tf_idf


def compute_doc_vectors(complete_set, tf_idf_matrix, tokens):
    doc_vectors = defaultdict(tuple)
    for doc_id in complete_set:
        vector = []
        for token in tokens:
            set_of_docweights = tf_idf_matrix[token]
            weight = set_of_docweights[doc_id]
            vector.append(weight)
        doc_vectors[doc_id] = vector
    return doc_vectors


def compute_vector_scores
