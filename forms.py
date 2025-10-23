# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    """Form for users to create a new account."""
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', 
                       choices=[('User', 'User'), ('Technician', 'Technician'), ('Admin', 'Admin')], 
                       validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Check if username already exists."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """Form for users to login."""
    username = StringField('Username', 
                           validators=[DataRequired()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    submit = SubmitField('Login')

class KBSearchForm(FlaskForm):
    """Form for searching the knowledge base."""
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class ArticleForm(FlaskForm):
    """Form for creating or editing a KB article."""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=150)])
    # We will populate choices for 'category' dynamically in the route
    category = SelectField('Category', choices=[
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Network', 'Network'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Article')