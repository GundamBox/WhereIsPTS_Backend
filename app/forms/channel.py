from flask import current_app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import BooleanField, DecimalField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, ValidationError


class CreateChannelForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])

class UpdateChannelForm(FlaskForm):
    name = StringField(label='name')
