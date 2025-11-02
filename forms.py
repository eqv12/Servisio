# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from models import User

# --- This form is for PUBLIC registration ---
class RegistrationForm(FlaskForm):
    """Form for users to create a new account."""
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', 
                       choices=[('User', 'User'), ('Technician', 'Technician')], 
                       validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Check if username already exists."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Check if email already exists."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

# --- This form is for ADMINS to create users ---
class AdminCreateUserForm(FlaskForm):
    """Form for ADMINS to create a new account."""
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)])
    
    # --- THIS WAS THE MISSING FIELD ---
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    # ----------------------------------
    
    # Admins can create other Admins
    role = SelectField('Role', 
                       choices=[('User', 'User'), ('Technician', 'Technician'), ('Admin', 'Admin')], 
                       validators=[DataRequired()])
    submit = SubmitField('Create User')

    def validate_username(self, username):
        """Check if username already exists."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Check if email already exists."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

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
    category = SelectField('Category', choices=[
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Network', 'Network'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Article')

# --- USER PORTAL TICKET FORMS ---

class PortalIncidentForm(FlaskForm):
    """Form for USERS to create an incident."""
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', 
                           choices=[('Network', 'Network'), ('Hardware', 'Hardware'), ('Software', 'Software'), ('Other', 'Other')],
                           validators=[DataRequired()])
    submit = SubmitField('Submit Incident')

class PortalServiceForm(FlaskForm):
    """Form for USERS to create a service request."""
    title = StringField('Title', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[DataRequired()])
    request_type = SelectField('Request Type', 
                               choices=[('Software', 'Software'), ('Hardware', 'Hardware'), ('Access', 'Access'), ('Other', 'Other')],
                               validators=[DataRequired()])
    submit = SubmitField('Submit Request')

# --- PASSWORD RESET FORMS ---

class RequestResetForm(FlaskForm):
    """Form to request a password reset email."""
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    """Form to actually change the password."""
    password = PasswordField('New Password', 
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

