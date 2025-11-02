"""
app.py - Main Flask Application
...
"""

from flask import Flask, redirect, url_for
from models import db
# --- Import your Config class ---
from config import Config
from routes.home import home_bp

# --- IMPORT FROM extensions.py ---
from extensions import db, bcrypt, login_manager, mail
# ---------------------------------

# --- CONFIGURE login_manager HERE ---
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
# ------------------------------------

# --- ADD USER LOADER ---
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    
    # --- LOAD ALL CONFIG FROM YOUR config.py FILE ---
    app.config.from_object(Config)
    # ------------------------------------------------
    
    # --- INITIALIZE EXTENSIONS WITH THE APP ---
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)  # <-- This initializes Flask-Mail
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
    from routes.admin import admin_bp 

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(incidents_bp, url_prefix='/admin/incidents')
    app.register_blueprint(services_bp, url_prefix='/admin/services')
    app.register_blueprint(kb_bp, url_prefix='/kb')
    app.register_blueprint(dashboard_bp, url_prefix='/admin/dashboard')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(portal_bp, url_prefix='/portal')
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)
    

    @app.route('/')
    def index():
        return redirect(url_for('home.home'))

    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all() 
        
    app.run(debug=True)

