# routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

# --- IMPORT FROM extensions.py ---
from extensions import db, bcrypt
# ---------------------------------
from models import User # We still need the User model
from forms import LoginForm, RegistrationForm


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        # If already logged in, send them to the right dashboard
        if current_user.role == 'User':
            return redirect(url_for('portal.portal_home'))
        return redirect(url_for('home.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(form.password.data):
            
            # --- NEW: CHECK IF USER IS APPROVED ---
            if not user.is_active:
                flash('Your account is pending admin approval. Please wait for an administrator to activate it.', 'warning')
                return redirect(url_for('auth.login'))
            # --- END OF NEW CHECK ---

            login_user(user) # This is the magic!
            flash('Login successful!', 'success')
            
            # --- ROLE-BASED REDIRECT ---
            if current_user.role == 'User':
                return redirect(url_for('portal.portal_home'))
            else:
                # Admin and Technician go to the admin-side home
                return redirect(url_for('home.home'))
            # ---------------------------
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')

    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/logout')
@login_required  # Can't logout if you aren't logged in
def logout():
    """Logs the current user out."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles new user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # --- UPDATED: Add email and set is_active to False ---
        user = User(
            username=form.username.data, 
            email=form.email.data,  # <-- Added email
            role=form.role.data,
            is_active=False  # <-- Account is inactive until approved
        )
        # ---------------------------------------------------
        
        user.set_password(form.password.data) # Use our hashing method
        db.session.add(user)
        db.session.commit()

        # --- UPDATED: New flash message ---
        flash('Your account has been created and is now pending admin approval.', 'info')
        # ----------------------------------
        
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)