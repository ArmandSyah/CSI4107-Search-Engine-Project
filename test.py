from preprocessing import UOPreprocessing
from dictionary import dictionary
from invertedindex import InvertedIndex
from booleanretrieval import BooleanRetrieval
from corpusacess import CorpusAccess
from vectorspacemodel import VectorSpaceModel
import json

if __name__ == "__main__":
    proc = UOPreprocessing.UOPreprocessing()
    proc.preprocess_collections()

    uo_dict = dictionary.Dictionary()
    uo_dict.make_dictionary()

    inverted_index = InvertedIndex.InvertedIndex()
    inv_ind = inverted_index.make_inverted_index()

    # corpus_access = CorpusAccess.CorpusAccess()
    # pprint.pprint(corpus_access.access(['CSI-1', 'CSI-2']))

    # v = VectorSpaceModel.VectorSpaceModel(inv_ind)
    # pprint.pprint(v.retrieve('programming languages imperative'))