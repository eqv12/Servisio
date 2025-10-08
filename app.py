"""
app.py - Main Flask Application

Purpose:
    Entry point for the SmartITSM application. Initializes the Flask app,
    registers all blueprints (modules), and sets global configuration.

Responsibilities:
    - Initialize Flask application
    - Register blueprints:
        * Auth
        * Incidents
        * Services
        * Knowledge Base
        * Dashboard
        * API
    - Provide a base route ("/") to verify the app is running
    - Serve as central location for future middleware, logging, or global features

Usage:
    Run this file to start the development server:
        python app.py
"""

from flask import Flask
from routes.auth import auth_bp
from routes.incidents import incidents_bp
from routes.services import services_bp
from routes.kb import kb_bp
from routes.dashboard import dashboard_bp
from routes.api import api_bp
from routes.portal import portal_bp
from models import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS



def create_app():
    """
    Factory function to create and configure the Flask app.
    Returns:
        app (Flask): Configured Flask application instance
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # TODO: Move to config.py for modularity
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    # Register blueprints for modular development
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(incidents_bp, url_prefix='/admin/incidents')
    app.register_blueprint(services_bp, url_prefix='/admin/services')
    app.register_blueprint(kb_bp, url_prefix='/kb')
    app.register_blueprint(dashboard_bp, url_prefix='/admin/dashboard')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(portal_bp, url_prefix='/portal')

    # Base route
    @app.route('/')
    def home():
        """Simple route to verify that the app is running."""
        return "Welcome to SmartITSM! Base Flask App Running."

    return app

if __name__ == '__main__':
    """
    Starts the Flask development server in debug mode.
    For production, configure a WSGI server (e.g., Gunicorn) instead.
    """
    app = create_app()
    app.run(debug=True)
