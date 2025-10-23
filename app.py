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
# from routes.services import services_bp
from routes.kb import kb_bp
# from routes.dashboard import dashboard_bp
from routes.api import api_bp
# from routes.portal import portal_bp
from models import db
# from routes.home import home_bp
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from routes.home import home_bp

# --- IMPORT FROM extensions.py ---
from extensions import db, bcrypt, login_manager
# --- CONFIGURE login_manager HERE ---
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
# ------------------------------------

# --- ADD USER LOADER ---
# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    # We must import User here to avoid circular imports
    from models import User
    return User.query.get(int(user_id))

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY 
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    
    # --- INITIALIZE EXTENSIONS WITH THE APP ---
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    # ------------------------------------------

    # --- IMPORT BLUEPRINTS *INSIDE* THE FACTORY ---
    from routes.auth import auth_bp
    from routes.incidents import incidents_bp
    from routes.services import services_bp
    from routes.kb import kb_bp
    from routes.dashboard import dashboard_bp
    from routes.api import api_bp
    from routes.portal import portal_bp
    from routes.home import home_bp
    # ----------------------------------------------

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(incidents_bp, url_prefix='/admin/incidents')
    app.register_blueprint(services_bp, url_prefix='/admin/services')
    app.register_blueprint(kb_bp, url_prefix='/kb')
    app.register_blueprint(dashboard_bp, url_prefix='/admin/dashboard')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(portal_bp, url_prefix='/portal')
    app.register_blueprint(home_bp)

    @app.route('/')
    def index():
        return redirect(url_for('home.home'))

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Optional: Create all tables if the db doesn't exist
    # You might already handle this in a seed script.
    with app.app_context():
        # This checks if the tables are already created before creating them
        # This is a simple way, for real production use Flask-Migrate
        db.create_all() 
        
    app.run(debug=True)