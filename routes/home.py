# routes/home.py

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required  # <-- IMPORT THESE

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required  # <-- PROTECT THE ROUTE
def home():
    """
    Role-aware landing page.
    Redirects 'User' roles to the portal.
    Shows admin/tech dashboard for others.
    """
    # --- ROLE-BASED REDIRECT ---
    if current_user.role == 'User':
        return redirect(url_for('portal.portal_home'))
    
    # Admins and Technicians will see home.html
    return render_template('home.html')