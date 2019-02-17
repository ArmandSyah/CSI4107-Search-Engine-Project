from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField('Search Field', validators=[DataRequired()])
    models = RadioField('Search Model', choices=[
                       ('b', 'Boolean Model'), ('v', 'Vector Space Model')], default='b', validators=[DataRequired()])
    submit = SubmitField('Submit')
