from flask import Flask
from preprocessing import UOPreprocessing
from dictionary import dictionary
from invertedindex import InvertedIndex
from booleanretrieval import BooleanRetrieval
from corpusacess import CorpusAccess
from vectorspacemodel import VectorSpaceModel

proc = UOPreprocessing.UOPreprocessing()
proc.preprocess_collections()

uo_dict = dictionary.Dictionary()
uo_dict.make_dictionary()

inverted_index = InvertedIndex.InvertedIndex()
inv_ind = inverted_index.make_inverted_index()

boolean_search = BooleanRetrieval.BooleanRetrieval(inv_ind)
vector_space_search = VectorSpaceModel.VectorSpaceModel(inv_ind)

corpus_access = CorpusAccess.CorpusAccess()

userinterface = Flask(__name__)
userinterface.config['SECRET_KEY'] = 'key'

from userinterface import routes
