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

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, ServiceRequest

services_bp = Blueprint('services', __name__, url_prefix='/admin/services')


@services_bp.route('/')
def list_services():
    """
    List all service requests from DB.
    """
    services = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
    return render_template('admin/services.html', services=services)

@services_bp.route('/create', methods=['GET', 'POST'])
def create_service():
    """Create a new service request"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        request_type = request.form.get('request_type')

        if not title or not description:
            flash("Title and description are required.", "danger")
            return redirect(url_for('services.create_service'))

        new_service = ServiceRequest(
            title=title,
            description=description,
            request_type=request_type,
            status='Pending',
            created_by=1  # placeholder until auth added
        )

        db.session.add(new_service)
        db.session.commit()
        flash("Service request created successfully!", "success")
        return redirect(url_for('services.list_services'))

    return render_template('admin/service_create.html')


"""
Developer Notes:
----------------
- This is the admin-side creation form.
- Later you can let users create requests through portal instead.
"""



"""
Developer Notes:
----------------
- ServiceRequest model fields expected: id, title, description, status, request_type, created_at, requested_by
- Add empty-state handling in template
- Later steps will add create/update/delete routes
"""
@services_bp.route('/update/<int:id>', methods=['POST'])
def update_service(id):
    """Update a service request's status"""
    service = ServiceRequest.query.get_or_404(id)
    new_status = request.form.get('status')

    if new_status and new_status != service.status:
        service.status = new_status
        db.session.commit()
        flash(f"Service request #{id} updated to '{new_status}'.", "success")

    return redirect(url_for('services.list_services'))


@services_bp.route('/delete/<int:id>', methods=['POST'])
def delete_service(id):
    """Delete a service request by ID"""
    service = ServiceRequest.query.get(id)
    if service:
        db.session.delete(service)
        db.session.commit()
        flash(f"Service request #{id} deleted successfully.", "success")
    else:
        flash("Service request not found.", "danger")

    return redirect(url_for('services.list_services'))
