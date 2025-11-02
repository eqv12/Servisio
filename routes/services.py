from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from models import db, ServiceRequest, WorkNote, User
from datetime import datetime
from flask_login import current_user, login_required
# --- IMPORT THE SERVICE ---
from services import service_request_service
from services.email_service import send_ticket_assigned_email

services_bp = Blueprint('services', __name__, url_prefix='/admin/services')

@services_bp.route('/')
@login_required
def list_services():
    # ... (This logic is fine) ...
    if current_user.role == 'Admin':
        services = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
    elif current_user.role == 'Technician':
        services = ServiceRequest.query.filter_by(assigned_to=current_user.id).order_by(ServiceRequest.created_at.desc()).all()
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('home.home'))
    return render_template('admin/services.html', services=services)

@services_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_service():
    if current_user.role not in ['Admin', 'Technician']:
        flash("You do not have permission to perform this action.", "danger")
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        request_type = request.form.get('request_type')

        if not title or not description:
            flash("Title and description are required.", "danger")
            return render_template('admin/service_create.html') # Return form

        # --- REFACTORED: Call the service ---
        # The service now handles auto-assignment, email, and db.commit()
        service, error, tech_name = service_request_service.create_service(
            title=title,
            description=description,
            request_type=request_type,
            user_id=current_user.id
        )
        
        if error:
            flash(error, "danger")
            return render_template('admin/service_create.html')

        flash(f"Service request created successfully! Assigned to {tech_name if tech_name else 'No available technician.'}", "success")
        return redirect(url_for('services.list_services'))

    return render_template('admin/service_create.html')

# ... (update_service and delete_service are fine) ...
@services_bp.route('/update/<int:id>', methods=['POST'])
@login_required
def update_service(id):
    # ... (This logic is fine) ...
    service = ServiceRequest.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status and new_status != service.status:
        service.status = new_status
        db.session.commit()
        flash(f"Service request #{id} updated to '{new_status}'.", "success")
    return redirect(request.referrer or url_for('services.list_services'))

@services_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_service(id):
    # ... (This logic is fine) ...
    if current_user.role != 'Admin':
        abort(403)
    service = ServiceRequest.query.get(id)
    if service:
        if service.assigned_to:
            tech = User.query.get(service.assigned_to)
            if tech and tech.workload > 0:
                tech.workload -= 1
        db.session.delete(service)
        db.session.commit()
        flash(f"Service request #{id} deleted successfully.", "success")
    else:
        flash("Service request not found.", "danger")
    return redirect(url_for('services.list_services'))


@services_bp.route('/<int:id>')
@login_required
def view_service(id):
    # ... (This logic is fine) ...
    service = ServiceRequest.query.get_or_404(id)
    work_notes = service.work_notes.order_by(WorkNote.created_at.desc()).all()
    technicians = User.query.filter_by(role='Technician').all()
    return render_template('admin/service_detail.html', service=service, work_notes=work_notes, technicians=technicians)

@services_bp.route('/<int:id>/add_note', methods=['POST'])
@login_required
def add_work_note(id):
    # ... (This logic is fine) ...
    note_text = request.form.get('note')
    if not note_text:
        flash("Work note cannot be empty.", "danger")
        return redirect(url_for('services.view_service', id=id))

    new_note = WorkNote(
        service_request_id=id,
        technician_id=current_user.id,
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
    if current_user.role != 'Admin':
        abort(403)
    service = ServiceRequest.query.get_or_404(id)
    technician_id = request.form.get('technician_id')

    new_tech = User.query.get(technician_id)
    # ... (validation is fine) ...

    # --- UPDATED: Email logic ---
    old_tech_id = service.assigned_to
    if old_tech_id and old_tech_id != new_tech.id:
        old_tech = User.query.get(old_tech_id)
        if old_tech and old_tech.workload > 0:
            old_tech.workload -= 1
            
    new_tech.workload += 1
    service.assigned_to = new_tech.id
    db.session.commit()

    # Send email *after* commit
    send_ticket_assigned_email(new_tech, service)
    # ----------------------------

    flash(f"Service request reassigned to {new_tech.username}.", "success")
    return redirect(url_for('services.view_service', id=id))

@services_bp.route('/approve/<int:id>', methods=['POST'])
@login_required
def approve_service(id):
    if current_user.role != 'Admin':
        abort(403)
    service = ServiceRequest.query.get_or_404(id)
    service.approval_status = 'Approved'
    service.approved_by = current_user.id
    service.approved_at = datetime.now()

    # Check if it's *already* assigned. If not, auto-assign.
    technician = None
    if not service.assigned_to:
        technician = User.query.filter_by(role='Technician', team=service.request_type).order_by(User.workload.asc()).first()
        if technician:
            service.assigned_to = technician.id
            technician.workload += 1

    db.session.commit()
    
    # --- UPDATED: Email logic ---
    if technician:
        send_ticket_assigned_email(technician, service)
    # ----------------------------
    
    flash(f"Service request '{service.title}' approved successfully!", "success")
    return redirect(request.referrer or url_for('services.list_services'))

@services_bp.route('/reject/<int:id>', methods=['POST'])
@login_required
def reject_service(id):
    # ... (This logic is fine) ...
    if current_user.role != 'Admin':
        abort(403)
    service = ServiceRequest.query.get_or_404(id)
    service.approval_status = 'Rejected'
    service.status = 'Closed'
    service.approved_by = current_user.id
    service.approved_at = datetime.now()

    # If it was assigned, reduce workload
    if service.assigned_to:
        tech = User.query.get(service.assigned_to)
        if tech and tech.workload > 0:
            tech.workload -= 1
            service.assigned_to = None # Unassign
            
    db.session.commit()
    
    flash(f"Service request '{service.title}' has been rejected.", "danger")
    return redirect(request.referrer or url_for('services.list_services'))

