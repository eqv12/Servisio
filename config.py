"""
config.py - Application Configuration

Purpose:
    Centralized configuration for SmartITSM.

Responsibilities:
    - Store secret keys, database URI, and other environment settings
    - Define roles and permissions
    - Provide configuration constants for use across the app

Usage:
    Import config variables into app.py or other modules as needed.
"""

import os

# Flask secret key for sessions
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database URI (using SQLite for development)
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///servisio.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User roles
ROLES = {
    'ADMIN': 'Admin',
    'TECH': 'Technician',
    'USER': 'User'
}

# Other configurations can be added here

import os
from dotenv import load_dotenv

# Find the absolute path of the root directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Load the .env file from the root directory
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Set Flask configuration variables from .env file."""
    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Gemini API Key
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')