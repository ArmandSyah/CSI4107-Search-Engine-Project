from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField('Search Field', validators=[DataRequired()])
    models = RadioField('Search Model', choices=[
                       ('b', 'Boolean Model'), ('v', 'Vector Space Model')], default='b', validators=[DataRequired()])
    dictionary_modes = RadioField('Dictionary Mode', choices=[('unaltered', 'Unaltered'), ('fully_altered', 'Fully Altered'), (
        'stopwords_removed', 'Stopwords Removed'), ('stemmed', 'Stemmed'), ('normalized', 'Normalized')], default='unaltered', validators=[DataRequired()])
    submit = SubmitField('Submit')
