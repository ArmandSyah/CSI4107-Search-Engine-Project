# Sets up the search engine modules and the Flask package that will be used to build our user interface
# Modified from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


from flask import Flask

from booleanretrievalmodel import BooleanRetrievalModel
from corpusacess import CorpusAccess
from vectorspacemodel import VectorSpaceModel
from invertedindex import InvertedIndex
from bigrammodels import BigramModel
from timeit import default_timer as timer

import click
import json

userinterface = Flask(__name__)
userinterface.config['SECRET_KEY'] = 'key'
userinterface.add_template_global(name='zip', f=zip)

with open('bigram_model.json') as bigram_model:
    autocomplete_models = json.load(bigram_model)

boolean_search = BooleanRetrievalModel.BooleanRetrievalModel()

start = timer()
print("setting up vector space model")
vector_space_search = VectorSpaceModel.VectorSpaceModel()
end = timer()
print("finished setting up vector space model")
print(f"{end - start} seconds")

corpus_access = CorpusAccess.CorpusAccess()

print("ui ready")

from userinterface import routes
