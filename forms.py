from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

# app = Flask(__name__)

class Registration(FlaskForm):
    email = StringField('Email',
                         validators=[DataRequired()])
    password = StringField('Password', 
                            validators=[DataRequired()])

    confirm_password = StringField('Confirm Password',
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