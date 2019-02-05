from preprocessing import UOPreprocessing
from dictionary import dictionary
from invertedindex import InvertedIndex
import json

if __name__ == "__main__":
    proc = UOPreprocessing.UOPreprocessing()
    proc.preprocess_collections()

    uo_dict = dictionary.Dictionary()
    uo_dict.make_dictionary()

    inverted_index = InvertedIndex.InvertedIndex()
    inverted_index.make_inverted_index()
