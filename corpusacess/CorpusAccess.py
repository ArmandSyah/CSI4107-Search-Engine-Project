import json


class CorpusAccess():
    """
        Simple module that loads corpus json file, takes list of doc_ids and returns list of subsequent documents

    """

    def __init__(self):
        with open('corpus.json') as corpus:
            self.corpus = json.load(corpus)

        with open('updated_corpus_reuters_knn.json') as corpus:
            self.corpus_reuters_knn = json.load(corpus)

        with open('updated_corpus_reuters_nb.json') as corpus:
            self.corpus_reuters_nb = json.load(corpus)

    def access(self, doc_ids, topic, classification):
        accessed_docs = [document for document in self.corpus if document['doc_id'] in doc_ids] + [
            document for document in (self.corpus_reuters_knn if classification == "knn" else self.corpus_reuters_nb) if document['doc_id'] in doc_ids]
        if (topic == "all"):
            return accessed_docs
        filtered_docs = [
            document for document in accessed_docs if document["topic"] == topic]
        return filtered_docs

    def get_doc(self, doc_id):
        accessed_docs = [document for document in self.corpus if document['doc_id'] in doc_id] + [
            document for document in self.corpus_reuters_knn if document['doc_id'] in doc_id] + [
            document for document in self.corpus_reuters_nb if document['doc_id'] in doc_id]
        return [document for document in accessed_docs if document['doc_id'] == doc_id][0]
