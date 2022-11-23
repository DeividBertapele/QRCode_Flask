from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class QRCodeData(FlaskForm):
    data = StringField('Data',
                       validators=[DataRequired(), 
                                   Length(min=1, max=250)])
    submit = SubmitField('Generate QRCode') 