# routes/services.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from models import db, ServiceRequest, WorkNote, User # Import User and WorkNote
from datetime import datetime
from flask_login import current_user

services_bp = Blueprint('services', __name__, url_prefix='/admin/services')

@services_bp.route('/')
def list_services():
    """ List all service requests from DB. """
    services = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
    return render_template('admin/services.html', services=services)

@services_bp.route('/create', methods=['GET', 'POST'])
def create_service():
    """Create a new service request"""
    if request.method == 'POST':
        # ... (your create logic is fine, but we update the object) ...
        title = request.form.get('title')
        description = request.form.get('description')
        request_type = request.form.get('request_type') # This is the "category"

        if not title or not description:
            flash("Title and description are required.", "danger")
            return redirect(url_for('services.create_service'))

        new_service = ServiceRequest(
            title=title,
            description=description,
            request_type=request_type,
            # --- UPDATED LOGIC ---
            status='Open',               # Work status is 'Open'
            approval_status='Pending',   # Approval status is 'Pending'
            # ---------------------
            created_by=current_user.id # Use logged-in user
        )
        db.session.add(new_service)
        db.session.commit()
        flash("Service request created and awaiting approval!", "success")
        return redirect(url_for('services.list_services'))

    return render_template('admin/service_create.html')

@services_bp.route('/update/<int:id>', methods=['POST'])
def update_service(id):
    """Update a service request's work status"""
    service = ServiceRequest.query.get_or_404(id)
    new_status = request.form.get('status') # This is for 'Open', 'In Progress', 'Resolved'

    if new_status and new_status != service.status:
        service.status = new_status
        db.session.commit()
        flash(f"Service request #{id} updated to '{new_status}'.", "success")
    
    # Redirect to detail view if it exists, otherwise list view
    return redirect(request.referrer or url_for('services.list_services'))

@services_bp.route('/delete/<int:id>', methods=['POST'])
def delete_service(id):
    """Delete a service request by ID"""
    service = ServiceRequest.query.get(id)
    if service:
        # You may want to delete related work notes here too
        db.session.delete(service)
        db.session.commit()
        flash(f"Service request #{id} deleted successfully.", "success")
    else:
        flash("Service request not found.", "danger")
    return redirect(url_for('services.list_services'))

# --- NEW DETAIL VIEW (Mirrors Incidents) ---
@services_bp.route('/<int:id>')
def view_service(id):
    """Detailed view of a service request with work notes."""
    service = ServiceRequest.query.get_or_404(id)
    # We will re-use WorkNote for this, but need to adapt it.
    # For now, let's just get technicians for assignment.
    technicians = User.query.filter_by(role='Technician').all()
    # Note: WorkNotes are tied to `incident_id`. You'd need to adapt the WorkNote model
    # to handle both incidents and services (polymorphic relationship) or create a
    # new `ServiceWorkNote` model. For now, we'll leave notes out.
    return render_template('admin/service_detail.html', service=service, technicians=technicians)

@services_bp.route('/assign/<int:id>', methods=['POST'])
def assign_technician(id):
    """Assign or reassign a service request to a technician."""
    service = ServiceRequest.query.get_or_404(id)
    technician_id = request.form.get('technician_id')

    if not technician_id:
        flash("Please select a technician.", "warning")
        return redirect(url_for('services.view_service', id=id))

    new_tech = User.query.get(technician_id)
    if not new_tech:
        flash("Invalid technician selected.", "danger")
        return redirect(url_for('services.view_service', id=id))

    # Adjust workload counters
    if service.assigned_to and service.assigned_to != new_tech.id:
        old_tech = User.query.get(service.assigned_to)
        if old_tech and old_tech.workload > 0:
            old_tech.workload -= 1
    new_tech.workload += 1

    service.assigned_to = new_tech.id
    db.session.commit()
    flash(f"Service request reassigned to {new_tech.username}.", "success")
    return redirect(url_for('services.view_service', id=id))

@services_bp.route('/approve/<int:id>', methods=['POST'])
def approve_service(id):
    """Approve a service request (Admin/Manager only)."""
    if current_user.role not in ['Admin', 'Manager']:
        abort(403)

    service = ServiceRequest.query.get_or_404(id)
    service.approval_status = 'Approved'
    service.approved_by = current_user.id
    service.approved_at = datetime.now()

    # Auto-assign technician after approval
    technician = User.query.filter_by(role='Technician', team=service.request_type).order_by(User.workload.asc()).first()
    if technician:
        service.assigned_to = technician.id
        technician.workload += 1
        
    db.session.commit()
    flash(f"Service request '{service.title}' approved successfully!", "success")
    return redirect(request.referrer or url_for('services.list_services'))

@services_bp.route('/reject/<int:id>', methods=['POST'])
def reject_service(id):
    """Reject a service request (Admin/Manager only)."""
    if current_user.role not in ['Admin', 'Manager']:
        abort(403)

    service = ServiceRequest.query.get_or_404(id)
    service.approval_status = 'Rejected'
    service.status = 'Closed' # Also close the work status
    service.approved_by = current_user.id
    service.approved_at = datetime.now()
    db.session.commit()
    flash(f"Service request '{service.title}' has been rejected.", "danger")
    return redirect(request.referrer or url_for('services.list_services'))