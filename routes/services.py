from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from models import db, ServiceRequest, WorkNote, User # Import WorkNote and User
from datetime import datetime
from flask_login import current_user, login_required

services_bp = Blueprint('services', __name__, url_prefix='/admin/services')

@services_bp.route('/')
@login_required
def list_services():
# ... (existing code) ...
    if current_user.role == 'Admin':
        services = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
    elif current_user.role == 'Technician':
# ... (existing code) ...
        services = ServiceRequest.query.filter_by(assigned_to=current_user.id).order_by(ServiceRequest.created_at.desc()).all()
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('home.home'))
    return render_template('admin/services.html', services=services)

@services_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_service():
# ... (existing code) ...
    if current_user.role not in ['Admin', 'Technician']:
        flash("You do not have permission to perform this action.", "danger")
        return redirect(url_for('home.home'))

    if request.method == 'POST':
# ... (existing code) ...
        title = request.form.get('title')
        description = request.form.get('description')
        request_type = request.form.get('request_type')

        if not title or not description:
# ... (existing code) ...
            flash("Title and description are required.", "danger")
            return redirect(url_for('services.create_service'))

        new_service = ServiceRequest(
# ... (existing code) ...
            title=title,
            description=description,
            request_type=request_type,
            status='Open',
            approval_status='Pending',
            created_by=current_user.id 
        )
        db.session.add(new_service)
# ... (existing code) ...
        db.session.commit()
        flash("Service request created successfully!", "success")
        return redirect(url_for('services.list_services'))

    return render_template('admin/service_create.html')

@services_bp.route('/update/<int:id>', methods=['POST'])
@login_required
def update_service(id):
# ... (existing code) ...
    service = ServiceRequest.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status and new_status != service.status:
# ... (existing code) ...
        service.status = new_status
        db.session.commit()
        flash(f"Service request #{id} updated to '{new_status}'.", "success")
    return redirect(request.referrer or url_for('services.list_services'))

@services_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_service(id):
# ... (existing code) ...
    if current_user.role != 'Admin':
        abort(403)
    service = ServiceRequest.query.get(id)
# ... (existing code) ...
    if service:
        db.session.delete(service)
        db.session.commit()
        flash(f"Service request #{id} deleted successfully.", "success")
    else:
        flash("Service request not found.", "danger")
# ... (existing code) ...
    return redirect(url_for('services.list_services'))

@services_bp.route('/<int:id>')
@login_required
def view_service(id):
    """Detailed view of a service request with work notes."""
    service = ServiceRequest.query.get_or_404(id)
    
    # --- UPDATED: Use the new relationship ---
    work_notes = service.work_notes.order_by(WorkNote.created_at.desc()).all()
    # -----------------------------------------
    
    technicians = User.query.filter_by(role='Technician').all()
    return render_template('admin/service_detail.html', service=service, work_notes=work_notes, technicians=technicians)

@services_bp.route('/<int:id>/add_note', methods=['POST'])
@login_required
def add_work_note(id):
    """Add a new technician work note to a service request."""
    note_text = request.form.get('note')
    technician_id = current_user.id

    if not note_text:
        flash("Work note cannot be empty.", "danger")
        return redirect(url_for('services.view_service', id=id))

    new_note = WorkNote(
        # --- UPDATED: Use specific foreign key ---
        service_request_id=id,
        # -----------------------------------------
        technician_id=technician_id,
        note=note_text,
        created_at=datetime.now()
    )
    db.session.add(new_note)
    db.session.commit()
    flash("Work note added successfully!", "success")
    return redirect(url_for('services.view_service', id=id))

@services_bp.route('/assign/<int:id>', methods=['POST'])
@login_required
def assign_technician(id):
# ... (existing code) ...
    if current_user.role != 'Admin':
        abort(403) # <-- Corrected typo 4G3 to 403
    service = ServiceRequest.query.get_or_404(id)
# ... (existing code) ...
    technician_id = request.form.get('technician_id')

    if not technician_id:
        flash("Please select a technician.", "warning")
# ... (existing code) ...
        return redirect(url_for('services.view_service', id=id))

    new_tech = User.query.get(technician_id)
    if not new_tech:
# ... (existing code) ...
        flash("Invalid technician selected.", "danger")
        return redirect(url_for('services.view_service', id=id))

    if service.assigned_to and service.assigned_to != new_tech.id:
# ... (existing code) ...
        old_tech = User.query.get(service.assigned_to)
        if old_tech and old_tech.workload > 0:
            old_tech.workload -= 1
    new_tech.workload += 1

    service.assigned_to = new_tech.id
# ... (existing code) ...
    db.session.commit()
    flash(f"Service request reassigned to {new_tech.username}.", "success")
    return redirect(url_for('services.view_service', id=id))

@services_bp.route('/approve/<int:id>', methods=['POST'])
@login_required
def approve_service(id):
# ... (existing code) ...
    if current_user.role != 'Admin':
        abort(403)
    service = ServiceRequest.query.get_or_404(id)
# ... (existing code) ...
    service.approval_status = 'Approved'
    service.approved_by = current_user.id
    service.approved_at = datetime.now()

    technician = User.query.filter_by(role='Technician', team=service.request_type).order_by(User.workload.asc()).first()
# ... (existing code) ...
    if technician:
        service.assigned_to = technician.id
        technician.workload += 1
    db.session.commit()
    
    flash(f"Service request '{service.title}' approved successfully!", "success")
# ... (existing code) ...
    return redirect(request.referrer or url_for('services.list_services'))

@services_bp.route('/reject/<int:id>', methods=['POST'])
@login_required
def reject_service(id):
# ... (existing code) ...
    if current_user.role != 'Admin':
        abort(403)
    service = ServiceRequest.query.get_or_404(id)
# ... (existing code) ...
    service.approval_status = 'Rejected'
    service.status = 'Closed'
    service.approved_by = current_user.id
    service.approved_at = datetime.now()
# ... (existing code) ...
    db.session.commit()
    
    flash(f"Service request '{service.title}' has been rejected.", "danger")
    return redirect(request.referrer or url_for('services.list_services'))

