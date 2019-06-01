from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class VoteForm(FlaskForm):
    cid = IntegerField(label='cid', validators=[DataRequired()])
