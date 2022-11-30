from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, EqualTo, Length
from photoapp.model import User

# app = Flask(__name__)

class Registration(FlaskForm):
    username = StringField('User Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                         validators=[DataRequired()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    fname = StringField('First Name',
                         validators=[DataRequired()])
    lname = StringField('Last Name',  
                         validators=[DataRequired()]) 

    submit = SubmitField('Create New Account')

class Login(FlaskForm):
    email = StringField('Email',
                         validators=[DataRequired()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddComment(FlaskForm):
    comment = StringField('Add Comment')
    submit = SubmitField('Submit')
    
