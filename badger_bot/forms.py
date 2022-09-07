from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class BadgerForm(FlaskForm):
    phone = StringField('phone', validators=[DataRequired()])
    content = TextAreaField('Focus', validators=[DataRequired()])
    submit = SubmitField('Badger')
