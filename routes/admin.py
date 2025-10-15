# # routes/admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.auth_service import db, User, roles_required
from models import ServiceRequest  # Optional — only if you have this table

# Blueprint registration
admin_bp = Blueprint("admin", __name__, template_folder="templates", url_prefix="/admin")


# -------------------- ADMIN DASHBOARD --------------------
@admin_bp.route("/dashboard")
@login_required
@roles_required("Admin")
def dashboard():
    """Admin dashboard showing summary statistics."""
    # Count user-related data
    total_users = User.query.count()
    total_technicians = User.query.filter_by(role="Technician").count()
    total_admins = User.query.filter_by(role="Admin").count()

    # Count service-related data if ServiceRequest table exists
    try:
        total_tickets = ServiceRequest.query.count()
        open_tickets = ServiceRequest.query.filter(ServiceRequest.status != "Resolved").count()
        resolved_tickets = ServiceRequest.query.filter_by(status="Resolved").count()
    except Exception:
        # If ServiceRequest not available, use defaults
        total_tickets = 0
        open_tickets = 0
        resolved_tickets = 0

    # Prepare dashboard statistics
    stats = {
        "total_users": total_users,
        "total_technicians": total_technicians,
        "total_admins": total_admins,
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "avg_resolution_time": "N/A"
    }

    users = User.query.all()

    # ✅ Important: pass `stats` to template
    return render_template(
        "admin/dashboard.html",
        users=users,
        stats=stats
    )

@admin_bp.route("/add_user", methods=["POST"])
@login_required
@roles_required("Admin")
def add_user_form():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    role = request.form.get("role")

    if User.query.filter_by(username=username).first():
        flash("Username already exists", "danger")
        return redirect(url_for("admin.dashboard"))
    
    

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    try:
        db.session.add(new_user)
        db.session.commit()
        flash(f"User '{username}' added as {role}", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
    finally:
        db.session.close()

    flash(f"User '{username}' added as {role}", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/dashboard_data")
@login_required
@roles_required("Admin")
def dashboard_data():
    """Provide JSON data for live dashboard charts."""

    # Incident chart data (dummy values — replace later)
    incident_labels = ["Open", "In Progress", "Resolved"]
    incident_values = [5, 3, 8]

    # Service chart data (dummy values — replace later)
    service_labels = ["Pending", "In Progress", "Approved", "Resolved"]
    service_values = [4, 6, 2, 10]

    return jsonify({
        "incident_labels": incident_labels,
        "incident_values": incident_values,
        "service_labels": service_labels,
        "service_values": service_values
    })


# -------------------- ADD USER (ADMIN ONLY) --------------------
@admin_bp.route("/add_user", methods=["POST"])
@login_required
@roles_required("Admin")
def add_user():
    """Admin adds a new user."""
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    role = request.form.get("role")

    # Validate unique username
    if User.query.filter_by(username=username).first():
        flash("Username already exists", "danger")
        return redirect(url_for("admin.dashboard"))

    # Create and save new user
    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash(f"User '{username}' added as {role}", "success")
    return redirect(url_for("admin.dashboard"))
