from flask_wtf import FlaskForm
from wtforms import StringField,DateTimeField,TextAreaField,SelectField,SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.csrf import CSRFProtect
from wtforms.fields import DateTimeLocalField
from flask import Flask

# csrf protection
csrf = CSRFProtect()
app = Flask(__name__)
csrf.init_app(app)


# created a form class for the assessment form that matches the database
# the form has the same fields as the database table and same data types
# has error checking to make sure data is present and of appropiate format
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class OpenPackForm (FlaskForm):
    submit = SubmitField('Open Pack')