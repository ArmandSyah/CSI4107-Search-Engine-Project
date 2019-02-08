import json
import math
from collections import defaultdict

# tf uses raw frequencies


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


def compute_idf(complete_set, inverted_index):
    number_of_docs = len(complete_set)
    return {word: math.log10(number_of_docs/len(docs))
            for word, docs in inverted_index.items()}


def compute_tf_idf(complete_set, inverted_index, idf_index):
    tf_idf = {}
    for word, docs in inverted_index.items():
        placeholder = defaultdict(int)
        for appearance in docs:
            placeholder[appearance.doc_id] = appearance.frequency * \
                idf_index[word]
        tf_idf[word] = placeholder
    return tf_idf
