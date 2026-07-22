from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import database as db
from app.dbmodels import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

# When any methods that match the pattern validate_<field_name> are added, 
# WTForms takes those as custom validators and invokes them in addition to 
# the stock validators. In this case I'd like to make sure that the username
# and email address entered by the user arn't already in the database, 
# otherwise if it exists a validation error will be triggered by raising an 
# exeption of type "ValidationError" and the message included as argument in 
# exeption will be the message displayed next to the field for the user to see.
    def validate_username(self, username):
        # Using .scalar instead of .scalars to return only the first result or None
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    # Override the constructor to save the original username as an environment variable for future verification
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
    
    # Simple validation of username, not really intended for busy applications when two or more
    # processes are accessing the database at the same time may cause the validation to pass
    # Validate username only if it was changed from the original username.
    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')