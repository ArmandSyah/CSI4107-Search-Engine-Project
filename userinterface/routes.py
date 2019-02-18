from flask import render_template, redirect
from userinterface import userinterface, boolean_search, vector_space_search, corpus_access
from userinterface.forms import SearchForm


@userinterface.route('/', methods=['GET', 'POST'])
@userinterface.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_results, scores = perform_search(
            form.search.data, form.models.data, form.dictionary_modes.data)
        # print(search_results)
        # print(scores)
        return render_template('results.html', results=search_results, model=form.models.data, scores=scores, query=form.search.data)
    return render_template('search.html', form=form)


@userinterface.route('/result/<doc_id>')
def get_result(doc_id):
    return render_template('result.html', result=corpus_access.access([doc_id])[0])


def perform_search(query, model, mode):
    if (model == 'b'):
        return corpus_access.access(boolean_search.retrieve(query, mode)), []
    else:
        retrieved = vector_space_search.retrieve(query, mode)
        docs, scores = [doc[0] for doc in retrieved], [doc[1]
                                                       for doc in retrieved]
        return corpus_access.access(docs), scores
