from flask import Blueprint, render_template
from flask_login import current_user, current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    """
    Role-aware landing page.
    Displays navigation cards to all major modules.
    """
    # In the future, you can customize based on role:
    # if current_user.is_authenticated and current_user.role == 'Technician':
    #     return redirect(url_for('incidents.list_incidents'))

    return render_template('home.html')
