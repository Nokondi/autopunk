from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import *
from google.cloud import datastore, ndb
ds_client = datastore.Client()
ndb_client = ndb.Client()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        with ndb_client.context():
            query = User.query(User.username==username.data)
            for u in query:
                if u.username == username.data:
                    raise ValidationError('Please use a different username.')


    def validate_email(self, email):
        with ndb_client.context():
            query = User.query(User.email==email.data)
            for u in query:
                if u.email == email.data:
                    raise ValidationError('Please use a different email address.')