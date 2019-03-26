# Sets up the search engine modules and the Flask package that will be used to build our user interface
# Modified from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


from flask import Flask

from booleanretrievalmodel import BooleanRetrievalModel
from corpusacess import CorpusAccess
from vectorspacemodel import VectorSpaceModel

import click

userinterface = Flask(__name__)
userinterface.config['SECRET_KEY'] = 'key'
userinterface.add_template_global(name='zip', f=zip)


print("start")


print("finished inverted index")

boolean_search = BooleanRetrievalModel.BooleanRetrievalModel(inv_ind)
vector_space_search = VectorSpaceModel.VectorSpaceModel(inv_ind)

corpus_access = CorpusAccess.CorpusAccess()

print("ui ready")

from userinterface import routes
