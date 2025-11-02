from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required

from extensions import db, bcrypt
from models import User
from services.email_service import send_new_user_alert
from forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from services.email_service import send_new_user_alert, send_password_reset_email

auth_bp = Blueprint('auth', __name__)

# ... (login and logout routes are fine) ...

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        if current_user.role == 'User':
            return redirect(url_for('portal.portal_home'))
        return redirect(url_for('home.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            
            if not user.is_active:
                flash('Your account is pending admin approval. Please wait for an administrator to activate it.', 'warning')
                return redirect(url_for('auth.login'))

            login_user(user)
            flash('Login successful!', 'success')
            
            if current_user.role == 'User':
                return redirect(url_for('portal.portal_home'))
            else:
                return redirect(url_for('home.home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')

    return render_template('auth/login.html', title='Login', form=form, show_reset_link=True)

@auth_bp.route('/logout')
@login_required
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
        user = User(
            username=form.username.data, 
            email=form.email.data,
            role=form.role.data,
            is_active=False
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # --- 2. FIND ADMINS AND SEND EMAIL ---
        try:
            # Find all active admins to notify them
            admins = User.query.filter_by(role='Admin', is_active=True).all()
            if admins:
                send_new_user_alert(admins, user)
            else:
                print("Registration successful, but no Admins found to notify.")
        except Exception as e:
            print(f"Error sending admin notification: {e}")
        # -----------------------------------
        
        flash('Your account has been created and is now pending admin approval.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/request_reset', methods=['GET', 'POST'])
def request_reset():
    """
    Route for user to request a password reset email.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('If an account with that email exists, a password reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/request_reset.html', title='Reset Password', form=form)


@auth_bp.route('/reset_token/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """
    Route for user to enter a new password using a valid token.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
        
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('auth.request_reset'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_token.html', title='Reset Your Password', form=form)

