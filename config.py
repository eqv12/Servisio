"""
config.py - Application Configuration

Purpose:
    Centralized configuration for SmartITSM.
    Loads settings from .env file into a Config class.
"""

import os
from dotenv import load_dotenv

# Find the absolute path of the root directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Load the .env file *before* anything else
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Set Flask configuration variables from .env file or defaults."""

    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-and-hard-to-guess-key'
    
    # # Database Config
    # # Default to a sqlite db inside an 'instance' folder
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'instance', 'servisio.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- DATABASE CONFIGURATION ---
    # Get the Database URL from the environment (Render will provide this)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # A common "gotcha": SQLAlchemy 1.4+ needs 'postgresql://'
    # but Render (and Heroku) provide 'postgres://'. This fixes it.
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///servisio.db' # Fallback to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gemini API Key
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # --- NEW MAIL SETTINGS ---
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # Set a default sender display name
    MAIL_DEFAULT_SENDER = ('Servisio Admin', os.environ.get('MAIL_USERNAME'))

# --- CONSTANTS ---
# (These are not config, so they can stay outside the class)
ROLES = {
    'ADMIN': 'Admin',
    'TECH': 'Technician',
    'USER': 'User'
}
