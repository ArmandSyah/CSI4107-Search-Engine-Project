from flask import render_template, redirect
from userinterface import userinterface, boolean_search, vector_space_search, corpus_access
from userinterface.forms import SearchForm


@userinterface.route('/', methods=['GET', 'POST'])
@userinterface.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_results = perform_search(form.search.data, 'b')
        return render_template('results.html', results=search_results)
    return render_template('search.html', form=form)


def perform_search(query, model):
    if (model == 'b'):
        return corpus_access.access(boolean_search.retrieve(query))
    else:
        return corpus_access.access(vector_space_search.retrieve(query))
