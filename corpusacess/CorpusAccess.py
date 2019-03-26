import json


class CorpusAccess():
    """
        Simple module that loads corpus json file, takes list of doc_ids and returns list of subsequent documents

    """

    def __init__(self):
        with open('corpus.json') as corpus:
            self.corpus = json.load(corpus)

        with open('corpus-reuters.json') as corpus:
            self.corpus_reuters = json.load(corpus)

    def access(self, doc_ids):
        return [document for document in self.corpus if document['doc_id'] in doc_ids] + [document for document in self.corpus_reuters if document['doc_id'] in doc_ids]
