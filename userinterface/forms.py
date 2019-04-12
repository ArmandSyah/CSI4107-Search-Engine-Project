from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired
import pickle


class SearchForm(FlaskForm):
    """
    The form class to represent a web form in a python class

    Form modified from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    """
    with open('list_of_topics.pickle', 'rb') as handle:
        topic_choices = pickle.load(handle)

    search = StringField('Search Field', validators=[
                         DataRequired()], id='search_autocomplete')
    models = RadioField('Search Model', choices=[
                       ('b', 'Boolean Model'), ('v', 'Vector Space Model')], default='b', validators=[DataRequired()])
    topic = SelectField('Choose Topic', choices=topic_choices)
    classification = RadioField('Select classification scheme', choices=[(
        'knn', 'K Nearest Neighbours'), ('nb', 'Naive Bayes')], default='knn', validators=[DataRequired()])
    dictionary_modes = RadioField('Dictionary Mode', choices=[('unaltered', 'Unaltered'), ('fully_altered', 'Fully Altered'), (
        'stopwords_removed', 'Stopwords Removed'), ('stemmed', 'Stemmed'), ('normalized', 'Normalized')], default='unaltered', validators=[DataRequired()])
    submit = SubmitField('Submit')
