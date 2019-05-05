from flask_wtf import FlaskForm, RecaptchaField
from wtforms import BooleanField, DecimalField, StringField, validators
from wtforms.validators import ValidationError


class CreateStoreForm(FlaskForm):
    name = StringField('name', [validators.DataRequired()])
    lat = DecimalField('lat', [validators.DataRequired()])
    lng = DecimalField('lng', [validators.DataRequired()])
    address = StringField('address', [validators.DataRequired()])
    switchable = StringField('switchable', [validators.DataRequired()])

    def validate_switchable(form, field):
        if field.data.lower() not in ('yes', 'true', 't', '1',
                                      'no', 'false', 'f', '0'):
            raise ValidationError('Invalid input syntax')

    recaptcha = RecaptchaField()


class UpdateStoreForm(FlaskForm):
    name = StringField('name')
    lat = DecimalField('lat')
    lng = DecimalField('lng')
    address = StringField('address')
    switchable = StringField('switchable')

    def validate_switchable(form, field):
        if field.data:
            if field.data.lower() not in ('yes', 'true', 't', '1',
                                          'no', 'false', 'f', '0'):
                raise ValidationError('Invalid input syntax')

    recaptcha = RecaptchaField()
