from flask import render_template, redirect
from userinterface import userinterface, boolean_search, vector_space_search, corpus_access
from userinterface.forms import SearchForm

# Controller functions to handle the routes for the user interface website and renders the html templates
# Modified from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms


@userinterface.route('/', methods=['GET', 'POST'])
@userinterface.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_results = perform_search(
            form.search.data, form.models.data, form.dictionary_modes.data)
        return render_template('results.html', results=search_results, model=form.models.data, query=form.search.data)
    return render_template('search.html', form=form)


@userinterface.route('/result/<doc_id>')
def get_result(doc_id):
    return render_template('result.html', result=corpus_access.access([doc_id])[0])


def perform_search(query, model, mode):
    if (model == 'b'):
        return corpus_access.access(boolean_search.retrieve(query, mode))
    else:
        retrieved = vector_space_search.retrieve(query, mode)
        results = []
        for doc_score_pair in retrieved:
            corpus_doc = corpus_access.access([doc_score_pair[0]])[0]
            corpus_doc['score'] = doc_score_pair[1]
            results.append(corpus_doc)

        return results
