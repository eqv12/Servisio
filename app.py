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

# --- Imports for Seeding ---
import os
from models import User
from extensions import bcrypt
# ---------------------------

# --- CONFIGURE login_manager HERE ---
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
# ------------------------------------

# --- ADD USER LOADER ---
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# --- NEW SEEDING FUNCTION ---
def _seed_database(app):
    """
    Checks if the database is empty and, if so, creates an admin account.
    This replaces the need for seed_admin.py on Render.
    """
    with app.app_context():
        # Create all tables if they don't exist
        db.create_all()
        
        # Check if any users already exist.
        if User.query.count() == 0:
            print("Database is empty. Seeding admin account...")
            
            # --- SET YOUR ADMIN DETAILS HERE ---
            ADMIN_USERNAME = 'admin'
            ADMIN_EMAIL = 'anony3938@gmail.com' # Using the email you provided
            ADMIN_PASSWORD = 'admin' # You can change this
            # -----------------------------------

            try:
                # Create the new admin user
                new_admin = User(
                    username=ADMIN_USERNAME,
                    email=ADMIN_EMAIL,
                    role='Admin',
                    is_active=True  # This is critical
                )
                
                # Set the password securely
                new_admin.set_password(ADMIN_PASSWORD)
                
                # Add to the database
                db.session.add(new_admin)
                db.session.commit()
                
                print(f"Admin user '{ADMIN_USERNAME}' created successfully!")
            except Exception as e:
                print(f"Error seeding database: {e}")
                db.session.rollback()
        else:
            print("Database already contains users. Skipping seed.")


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

    # --- MOVED SEEDING CALL HERE ---
    # This block will run once when the app starts on Render.
    _seed_database(app)
    # -------------------------------

    return app

# --- UPDATED MAIN RUN BLOCK ---
if __name__ == '__main__':
    app = create_app()
    
    # We can leave db.create_all() here for local development,
    # but the seed function already handles it.
    with app.app_context():
        db.create_all() 
        
    app.run(debug=True)

