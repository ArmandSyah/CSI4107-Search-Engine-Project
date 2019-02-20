# Sets up the search engine modules and the Flask package that will be used to build our user interface
# Modified from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


from flask import Flask
from preprocessing import UOPreprocessing
from dictionary import dictionary
from invertedindex import InvertedIndex
from booleanretrievalmodel import BooleanRetrievalModel
from corpusacess import CorpusAccess
from vectorspacemodel import VectorSpaceModel

proc = UOPreprocessing.UOPreprocessing()
proc.preprocess_collections()

uo_dict = dictionary.Dictionary()
uo_dict.make_dictionary()

inverted_index = InvertedIndex.InvertedIndex()
inv_ind = inverted_index.make_inverted_index()

boolean_search = BooleanRetrievalModel.BooleanRetrievalModel(inv_ind)
vector_space_search = VectorSpaceModel.VectorSpaceModel(inv_ind)

corpus_access = CorpusAccess.CorpusAccess()

userinterface = Flask(__name__)
userinterface.config['SECRET_KEY'] = 'key'
userinterface.add_template_global(name='zip', f=zip)

from userinterface import routes
