from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField
from passlib.hash import pbkdf2_sha256
from models import User


def invalid_credentials(form, field):
    password = field.data
    username = form.username.data
    
    user_data = User.query.filter_by(username=username).first()
    if user_data is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password, user_data.password):
        raise ValidationError("Username or password is incorrect")


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    email = EmailField("email", validators=[InputRequired("Please Enter valid email")])
    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Select a different username.")

class LoginForm(FlaskForm):

    username = StringField('username', validators=[InputRequired(message="Username required")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])

class Order(FlaskForm):
    name = StringField('name', validators=[InputRequired(message="work name required"), Length(min=6, max=20, message="The work name should be specified correctly minimum 6 words")])
    message = StringField('message', validators=[InputRequired(message="description required"), Length(min=15, max=120, message="description must be between 15 to 120 characters")])
    email = EmailField("email", validators=[InputRequired("Please Enter valid email")])
    #username = StringField('account', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])