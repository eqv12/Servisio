from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from extensions import db
from models import User
# --- Import the new form ---
from forms import AdminCreateUserForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/user_management')
@login_required
def user_management():
    """
    Admin-only page to view and approve users.
    """
    # Protect this route
    if current_user.role != 'Admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home.home'))

    # Get all users, showing inactive ones first
    all_users = User.query.order_by(User.is_active.asc(), User.username.asc()).all()
    
    return render_template('admin/user_management.html', users=all_users)

# --- NEW ROUTE FOR CREATING USERS ---
@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    """
    Admin-only route to manually create a new user.
    """
    if current_user.role != 'Admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('home.home'))
    
    form = AdminCreateUserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            role=form.role.data,
            is_active=True  # <-- Automatically active
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash(f"Account for '{user.username}' created successfully.", 'success')
        # TODO: Add email notification to the new user here
        
        return redirect(url_for('admin.user_management'))
    
    return render_template('admin/create_user.html', title='Create New User', form=form)
# --- END NEW ROUTE ---


@admin_bp.route('/approve_user/<int:user_id>', methods=['POST'])
@login_required
def approve_user(user_id):
    """
    Route for an Admin to approve a new user.
    """
    if current_user.role != 'Admin':
        abort(403) # Forbidden

    user = User.query.get_or_404(user_id)
    user.is_active = True
    db.session.commit()
    
    flash(f"User '{user.username}' has been approved and can now log in.", 'success')
    # TODO: Add email notification to the user here
    
    return redirect(url_for('admin.user_management'))

@admin_bp.route('/deactivate_user/<int:user_id>', methods=['POST'])
@login_required
def deactivate_user(user_id):
    """
    Route for an Admin to deactivate an existing user.
    """
    if current_user.role != 'Admin':
        abort(403)

    user = User.query.get_or_404(user_id)
    
    # Safety check: prevent admin from deactivating themselves
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'danger')
        return redirect(url_for('admin.user_management'))
        
    user.is_active = False
    db.session.commit()
    
    flash(f"User '{user.username}' has been deactivated and can no longer log in.", 'warning')
    return redirect(url_for('admin.user_management'))
