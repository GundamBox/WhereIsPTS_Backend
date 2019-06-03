from flask import current_app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (BooleanField, DecimalField, IntegerField, StringField,
                     validators)
from wtforms.validators import (DataRequired, NumberRange, Optional,
                                ValidationError)


class CreateStoreForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])
    lat = DecimalField(label='lat', validators=[DataRequired()])
    lng = DecimalField(label='lng', validators=[DataRequired()])
    address = StringField(label='address', validators=[DataRequired()])
    switchable = StringField(label='switchable', validators=[DataRequired()])

    def validate_switchable(form, field):
        if field.data.lower() not in ('yes', 'true', 't', '1',
                                      'no', 'false', 'f', '0'):
            raise ValidationError('Invalid input syntax')
        

    recaptcha = RecaptchaField()


class GetStoreListForm(FlaskForm):
    lat = DecimalField(label='lat',
                       validators=[DataRequired()])
    lng = DecimalField(label='lng',
                       validators=[DataRequired()])
    name = StringField(label='name',
                       default='')
    radius = DecimalField(label='radius',
                          validators=[NumberRange(min=current_app.config['STORE_SEARCH_MIN_RADIUS'],
                                                  max=current_app.config['STORE_SEARCH_MAX_RADIUS'])],
                          default=current_app.config['STORE_SEARCH_MIN_RADIUS'])
    page = IntegerField(label='page',
                        validators=[NumberRange(
                            min=current_app.config['STORE_SEARCH_DEFAULT_START_PAGE'])],
                        default=current_app.config['STORE_SEARCH_DEFAULT_START_PAGE'])
    page_size = IntegerField(label='page_size',
                             default=current_app.config['STORE_SEARCH_DEFAULT_PAGE_SIZE'])


class UpdateStoreForm(FlaskForm):
    name = StringField(label='name')
    lat = DecimalField(label='lat')
    lng = DecimalField(label='lng')
    address = StringField(label='address')
    switchable = StringField(label='switchable')

    def validate_switchable(form, field):
        if field.data:
            if field.data.lower() not in ('yes', 'true', 't', '1',
                                          'no', 'false', 'f', '0'):
                raise ValidationError('Invalid input syntax')

    recaptcha = RecaptchaField()
