# seed_admin.py
import os
from app import create_app
from extensions import db, bcrypt
from models import User

# --- SET YOUR ADMIN DETAILS HERE ---
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'anony3938@gmail.com'
ADMIN_PASSWORD = 'Admin123.' # Change this!
# -----------------------------------

app = create_app()

with app.app_context():
    # Check if the database file exists, if not, create it
    if not os.path.exists(os.path.join(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))):
        print("Creating new database...")
        db.create_all()

    # Check if admin user already exists
    admin_user = User.query.filter_by(username=ADMIN_USERNAME).first()

    if not admin_user:
        print(f"Creating new admin user: {ADMIN_USERNAME}...")
        
        # Create the new admin user
        new_admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            role='Admin',
            is_active=True  # <-- This is the key!
        )
        
        # Set the password securely
        new_admin.set_password(ADMIN_PASSWORD)
        
        # Add to the database
        db.session.add(new_admin)
        db.session.commit()
        
        print("Admin user created successfully!")
    else:
        print(f"Admin user '{ADMIN_USERNAME}' already exists.")