from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField("Phone", validators=[
        DataRequired(),
        Regexp(r'^[0-9]{10}$', message="Enter valid 10-digit phone number")
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField("Address")
    submit = SubmitField("Save")
