from preprocessing import UOPreprocessing
from dictionary import dictionary
from invertedindex import InvertedIndex
from booleanretrieval import BooleanRetrieval
import json

if __name__ == "__main__":
    proc = UOPreprocessing.UOPreprocessing()
    proc.preprocess_collections()

    uo_dict = dictionary.Dictionary()
    uo_dict.make_dictionary()

    inverted_index = InvertedIndex.InvertedIndex()
    inv_ind = inverted_index.make_inverted_index()

    b = BooleanRetrieval.BooleanRetrieval(inv_ind)
    import pprint
    pprint.pprint(b.retrieve('completed'))
