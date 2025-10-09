# """
# app.py - Main Flask Application

# Purpose:
#     Entry point for the SmartITSM application. Initializes the Flask app,
#     registers all blueprints (modules), and sets global configuration.

# Responsibilities:
#     - Initialize Flask application
#     - Register blueprints:
#         * Auth
#         * Incidents
#         * Services
#         * Knowledge Base
#         * Dashboard
#         * API
#     - Provide a base route ("/") to verify the app is running
#     - Serve as central location for future middleware, logging, or global features

# Usage:
#     Run this file to start the development server:
#         python app.py
# """

# from flask import Flask
# from routes.auth import auth_bp
# from routes.incidents import incidents_bp
# from routes.services import services_bp
# from routes.kb import kb_bp
# from routes.dashboard import dashboard_bp
# from routes.api import api_bp
# from routes.portal import portal_bp
# from models import db
# from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
# from flask_login import LoginManager
# from models import User


# def create_app():
#     """
#     Factory function to create and configure the Flask app.
#     Returns:
#         app (Flask): Configured Flask application instance
#     """
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'your-secret-key-here'  # TODO: Move to config.py for modularity
#     app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
#     db.init_app(app)

#     # ✅ Initialize Login Manager (Add this block here)
#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'  # Redirects to /auth/login if not logged in
#     login_manager.init_app(app)

#     # ✅ Define how to load a user from session
#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))

#     # Register blueprints for modular development
#     app.register_blueprint(auth_bp, url_prefix='/auth')
#     app.register_blueprint(incidents_bp, url_prefix='/admin/incidents')
#     app.register_blueprint(services_bp, url_prefix='/admin/services')
#     app.register_blueprint(kb_bp, url_prefix='/kb')
#     app.register_blueprint(dashboard_bp, url_prefix='/admin/dashboard')
#     app.register_blueprint(api_bp, url_prefix='/api')
#     app.register_blueprint(portal_bp, url_prefix='/portal')

#     # Base route
#     @app.route('/')
#     def home():
#         """Simple route to verify that the app is running."""
#         return "Welcome to SmartITSM! Base Flask App Running."

#     return app

# if __name__ == '__main__':
#     """
#     Starts the Flask development server in debug mode.
#     For production, configure a WSGI server (e.g., Gunicorn) instead.
#     """
#     app = create_app()      
#     app.run(debug=True)
"""
app.py - Main Flask Application

Purpose:
    Entry point for the SmartITSM application. Initializes the Flask app,
    registers all blueprints (modules), and sets global configuration.

Usage:
    Run this file to start the development server:
        python app.py
"""

from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes.auth import auth_bp
from routes.incidents import incidents_bp
from routes.services import services_bp
from routes.kb import kb_bp
from routes.dashboard import dashboard_bp
from routes.api import api_bp
from routes.portal import portal_bp
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

    # ✅ Initialize database
    db.init_app(app)
    #login_manager.init_app(app)

    # ✅ Initialize Login Manager (core Flask-Login setup)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to /auth/login when unauthorized
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    #✅ Tell Flask-Login how to load a user from the database
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ✅ Register all blueprints for modular routes
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(incidents_bp, url_prefix='/admin/incidents')
    app.register_blueprint(services_bp, url_prefix='/admin/services')
    app.register_blueprint(kb_bp, url_prefix='/kb')
    app.register_blueprint(dashboard_bp, url_prefix='/admin/dashboard')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(portal_bp, url_prefix='/portal')

    # ✅ Basic home route to confirm server is running
    @app.route('/')
    def home():
        """Simple route to verify that the app is running."""
        return "✅ SmartITSM Flask App is running successfully."

    return app


if __name__ == '__main__':
    """
    Starts the Flask development server in debug mode.
    For production, configure a WSGI server (e.g., Gunicorn) instead.
    """
    app = create_app()
    with app.app_context():
        # Ensure database tables exist before starting the server
        db.create_all()
    app.run(debug=True)
