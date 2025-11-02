from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from models import db, Incident, WorkNote, User
from datetime import datetime
from sqlalchemy import func
from flask_login import current_user, login_required
# --- IMPORT THE SERVICE ---
from services import incident_service
from services.email_service import send_ticket_assigned_email

incidents_bp = Blueprint('incidents', __name__, url_prefix='/admin/incidents')

@incidents_bp.route('/')
@login_required
def list_incidents():
    # ... (This logic is fine) ...
    if current_user.role == 'Admin':
        incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    elif current_user.role == 'Technician':
        incidents = Incident.query.filter_by(assigned_to=current_user.id).order_by(Incident.created_at.desc()).all()
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('home.home'))
    return render_template('admin/incidents.html', incidents=incidents)

@incidents_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_incident():
    if current_user.role not in ['Admin', 'Technician']:
        flash("You do not have permission to perform this action.", "danger")
        return redirect(url_for('home.home'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        priority = request.form['priority']
        
        # --- REFACTORED: Call the service ---
        # The service now handles auto-assignment, email, and db.commit()
        incident, error, tech_name = incident_service.create_incident(
            title=title,
            description=description,
            category=category,
            user_id=current_user.id,
            priority=priority  # Admin/Tech can set priority
        )
        
        if error:
            flash(error, "danger")
            # We must return the form on error
            return render_template('admin/incident_create.html') 
        
        flash(f"Incident created successfully! Assigned to {tech_name if tech_name else 'No available technician.'}", "success")
        return redirect(url_for('incidents.list_incidents'))
        
    return render_template('admin/incident_create.html')

# ... (update_incident and delete_incident are fine) ...
@incidents_bp.route('/update/<int:id>', methods=['POST'])
@login_required
def update_incident(id):
    # ... (This logic is fine) ...
    incident = Incident.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status and new_status != incident.status:
        incident.status = new_status
        db.session.commit()
        flash(f"Incident #{id} updated to '{new_status}'.", "success")
    return redirect(request.referrer or url_for('incidents.list_incidents')) # Use referrer

@incidents_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_incident(id):
    # ... (This logic is fine) ...
    if current_user.role != 'Admin':
        abort(403)
    incident = Incident.query.get(id)
    if incident:
        # We should also adjust workload if a tech had this ticket
        if incident.assigned_to:
            tech = User.query.get(incident.assigned_to)
            if tech and tech.workload > 0:
                tech.workload -= 1
        db.session.delete(incident)
        db.session.commit()
        flash(f"Incident #{id} deleted successfully.", "success")
    else:
        flash("Incident not found.", "danger")
    return redirect(url_for('incidents.list_incidents'))


@incidents_bp.route('/<int:id>')
@login_required
def view_incident(id):
    # ... (This logic is fine) ...
    incident = Incident.query.get_or_404(id)
    work_notes = incident.work_notes.order_by(WorkNote.created_at.desc()).all()
    technicians = User.query.filter_by(role='Technician').all()
    return render_template('admin/incident_detail.html', incident=incident, work_notes=work_notes, technicians=technicians)


@incidents_bp.route('/<int:id>/add_note', methods=['POST'])
@login_required
def add_work_note(id):
    # ... (This logic is fine) ...
    note_text = request.form.get('note')
    if not note_text:
        flash("Work note cannot be empty.", "danger")
        return redirect(url_for('incidents.view_incident', id=id))

    new_note = WorkNote(
        incident_id=id,
        technician_id=current_user.id,
        note=note_text,
        created_at=datetime.now()
    )
    db.session.add(new_note)
    db.session.commit()
    flash("Work note added successfully!", "success")
    return redirect(url_for('incidents.view_incident', id=id))

@incidents_bp.route('/assign/<int:id>', methods=['POST'])
@login_required
def assign_technician(id):
    if current_user.role != 'Admin':
        abort(403)
    incident = Incident.query.get_or_404(id)
    technician_id = request.form.get('technician_id')

    new_tech = User.query.get(technician_id)
    # ... (validation is fine) ...

    # --- UPDATED: Email logic ---
    old_tech_id = incident.assigned_to
    if old_tech_id and old_tech_id != new_tech.id:
        old_tech = User.query.get(old_tech_id)
        if old_tech and old_tech.workload > 0:
            old_tech.workload -= 1
    
    new_tech.workload += 1
    incident.assigned_to = new_tech.id
    db.session.commit()
    
    # Send email *after* commit
    send_ticket_assigned_email(new_tech, incident)
    # ----------------------------

    flash(f"Incident reassigned to {new_tech.username}.", "success")
    return redirect(url_for('incidents.view_incident', id=id))

@incidents_bp.route('/approve/<int:id>', methods=['POST'])
@login_required
def approve_incident(id):
    if current_user.role != 'Admin':
        abort(403)
    incident = Incident.query.get_or_404(id)
    incident.approval_status = 'Approved'
    incident.approved_by = current_user.id
    incident.approved_at = datetime.now()
    
    # Check if it's *already* assigned. If not, auto-assign.
    technician = None
    if not incident.assigned_to:
        technician = User.query.filter_by(role='Technician', team=incident.category)\
                             .order_by(User.workload.asc()).first()
        if technician:
            incident.assigned_to = technician.id
            technician.workload += 1
    
    db.session.commit()
    
    # --- UPDATED: Email logic ---
    if technician:
        send_ticket_assigned_email(technician, incident)
    # ----------------------------

    flash(f"Incident '{incident.title}' approved successfully!", "success")
    return redirect(url_for('incidents.view_incident', id=id))

@incidents_bp.route('/reject/<int:id>', methods=['POST'])
@login_required
def reject_incident(id):
    # ... (This logic is fine) ...
    if current_user.role != 'Admin':
        abort(403)
    incident = Incident.query.get_or_404(id)
    incident.approval_status = 'Rejected'
    incident.status = 'Closed' # Also close the work status
    incident.approved_by = current_user.id
    incident.approved_at = datetime.now()
    
    # If it was assigned, reduce workload
    if incident.assigned_to:
        tech = User.query.get(incident.assigned_to)
        if tech and tech.workload > 0:
            tech.workload -= 1
            incident.assigned_to = None # Unassign
            
    db.session.commit()

    flash(f"Incident '{incident.title}' has been rejected.", "danger")
    return redirect(url_for('incidents.view_incident', id=id))

