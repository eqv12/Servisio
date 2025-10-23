# extensions.py

"""
extensions.py - Centralized Flask Extensions

Purpose:
    Initializes all Flask extensions in one place to avoid circular imports.
    Other modules (app.py, models.py, routes) will import instances from this file.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()