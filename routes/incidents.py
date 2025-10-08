"""
routes/incidents.py
-------------------
Admin / Technician Module – Incident Management

Purpose:
    Displays all incidents from the database for the admin/technician panel.
    This is Step 3 of the Admin Module: Read Operations.

Responsibilities:
    - Query all incidents from DB
    - Render list in admin/incidents.html
    - Prepare for later CRUD additions (create, update, delete)
"""

from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Incident

incidents_bp = Blueprint('incidents', __name__, url_prefix='/admin/incidents')


@incidents_bp.route('/')
def list_incidents():
    """
    List all incidents from DB and render the admin template.
    """
    # Example: order by newest first
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()

    # Pass to template (Jinja can access model attributes directly)
    return render_template('admin/incidents.html', incidents=incidents)


# --- Placeholder for future CRUD routes (Steps 4–6) ---
# def create_incident(): ...
# def update_incident(): ...
# def delete_incident(): ...
# ------------------------------------------------------

"""
Developer Notes:
----------------
- Incident model fields expected: id, title, description, status, priority, created_at, created_by
- Add guards in template for optional fields (e.g., created_by might be None)
- This file now returns real DB data (no dummy lists)
"""
