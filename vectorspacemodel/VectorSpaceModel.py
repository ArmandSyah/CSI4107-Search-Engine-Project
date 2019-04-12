import json
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
from utilities import *
from collections import namedtuple


class VectorSpaceModel():
    """
    Implementation of the Vector Space Retrieval Model
    For my implementation, tf is simply the raw frequencies of the word in the document
    Assume all words in the query have an equal weight, 1
    """

    def __init__(self):
        with open('corpus.json') as corpus, open('corpus-reuters.json') as corpus_reuters:
            c = json.load(corpus)
            c_r = json.load(corpus_reuters)
            self.complete_set = {document['doc_id'] for document in c}
            self.complete_set |= {document['doc_id'] for document in c_r}
        with open('inverted_index.json') as inv_index:
            self.inverted_index = json.load(inv_index)
        with open('thesaurus.json') as thesaurus:
            self.thesaurus = json.load(thesaurus)
        self.mode = 'unaltered'
        self.tf_idf_matrix = compute_tf_idf(
            self.complete_set,
            self.inverted_index,
            compute_idf(self.complete_set, self.inverted_index))

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
        expanded_tokens, expanded_query_vector = self.expand_tokens_from_thesaurus(
            tokens, query_vector)

        doc_vectors = compute_doc_vectors(
            self.complete_set, self.tf_idf_matrix, expanded_tokens)

        return compute_vector_scores(expanded_query_vector, doc_vectors)

    def expand_tokens_from_thesaurus(self, tokens, query_vector):
        """Handles the expansion of the query. Uses the thesaurus made from before
            Iterates through all current tokens, check them against the thesaurus,
            takes the 2 related terms with the highest score
        """
        new_tokens, new_query_vector = [
            token for token in tokens], [v for v in query_vector]
        for token in tokens:
            if token not in self.thesaurus:
                continue
            related_terms = sorted(
                self.thesaurus[token].items(), key=lambda kv: kv[1], reverse=True)
            related_terms = related_terms[:(2 if len(
                related_terms) > 2 else len(related_terms) - 1)]
            import pprint
            pprint.pprint(related_terms)
            for related_term, score in related_terms:
                if related_term in new_tokens:
                    continue
                new_tokens.append(related_term)
                new_query_vector.append(score)
        show_new_query = zip(new_tokens, new_query_vector)
        new_query = f"New Query: {' '.join(f'{t[0]} ({t[1]})' for t in show_new_query)}"
        print(new_query)
        return new_tokens, new_query_vector


def compute_idf(complete_set, inverted_index):
    """
    Get the inverted index for each word
    """
    number_of_docs = len(complete_set)
    return {word: math.log10(number_of_docs / len(docs)) for word, docs in inverted_index.items()}


def compute_tf_idf(complete_set, inverted_index, idf_index):
    """
    Set up the TF-IDF matrix, indexed 2-dimensionally by word and then doc
    """
    tf_idf = defaultdict(lambda: defaultdict(int))
    for word, docs in inverted_index.items():
        placeholder = defaultdict(int)
        for appearance in docs:
            a = json.loads(appearance, object_hook=lambda d: namedtuple(
                'X', d.keys())(*d.values()))
            placeholder[a.doc_id] = a.frequency * \
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
