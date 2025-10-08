"""
routes/services.py
-------------------
Admin / Technician Module – Service Request Management

Purpose:
    Displays all service requests from the database.
    This completes Step 3 of the Admin Module: Read Operations.

Responsibilities:
    - Query all service requests
    - Render list in admin/services.html
"""

from flask import Blueprint, render_template
from models import db, ServiceRequest

services_bp = Blueprint('services', __name__, url_prefix='/admin/services')


@services_bp.route('/')
def list_services():
    """
    List all service requests from DB.
    """
    services = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
    return render_template('admin/services.html', services=services)



"""
Developer Notes:
----------------
- ServiceRequest model fields expected: id, title, description, status, request_type, created_at, requested_by
- Add empty-state handling in template
- Later steps will add create/update/delete routes
"""
