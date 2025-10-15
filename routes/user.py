# routes/user.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from services.auth_service import roles_required

user_bp = Blueprint("user", __name__, template_folder="templates", url_prefix="/user")

@user_bp.route("/dashboard")
@login_required
@roles_required("User")
def dashboard():
    return render_template("user/dashboard.html", user=current_user)
