from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from models import db, Incident, WorkNote, User
from datetime import datetime
from sqlalchemy import func
from flask_login import current_user, login_required

incidents_bp = Blueprint('incidents', __name__, url_prefix='/admin/incidents')

# ... (list_incidents, create_incident, update_incident, delete_incident are all fine) ...
@incidents_bp.route('/')
@login_required
def list_incidents():
# ... (existing code) ...
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
# ... (existing code) ...
    if current_user.role not in ['Admin', 'Technician']:
        flash("You do not have permission to perform this action.", "danger")
        return redirect(url_for('home.home'))
    if request.method == 'POST':
        title = request.form['title']
# ... (existing code) ...
        description = request.form['description']
        category = request.form['category']
        priority = request.form['priority']
        technician = User.query.filter_by(role='Technician', team=category).order_by(User.workload.asc()).first()
# ... (existing code) ...
        assigned_to = technician.id if technician else None
        new_incident = Incident(
            title=title,
# ... (existing code) ...
            description=description,
            category=category,
            priority=priority,
            status='Open',
            created_by=current_user.id, 
            assigned_to=assigned_to
        )
        db.session.add(new_incident)
        if technician:
            technician.workload += 1
# ... (existing code) ...
        db.session.commit()
        flash(f"Incident created successfully! Assigned to {technician.username if technician else 'No available technician.'}", "success")
        return redirect(url_for('incidents.list_incidents'))
    return render_template('admin/incident_create.html')

@incidents_bp.route('/update/<int:id>', methods=['POST'])
@login_required
def update_incident(id):
# ... (existing code) ...
    incident = Incident.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status and new_status != incident.status:
# ... (existing code) ...
        incident.status = new_status
        db.session.commit()
        flash(f"Incident #{id} updated to '{new_status}'.", "success")
    return redirect(url_for('incidents.list_incidents'))

@incidents_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_incident(id):
# ... (existing code) ...
    if current_user.role != 'Admin':
        abort(403)
    incident = Incident.query.get(id)
# ... (existing code) ...
    if incident:
        db.session.delete(incident)
        db.session.commit()
        flash(f"Incident #{id} deleted successfully.", "success")
    else:
        flash("Incident not found.", "danger")
    return redirect(url_for('incidents.list_incidents'))

@incidents_bp.route('/<int:id>')
@login_required
def view_incident(id):
    """Detailed view of an incident with work notes."""
    incident = Incident.query.get_or_404(id)
    
    # --- UPDATED: Use the new relationship ---
    work_notes = incident.work_notes.order_by(WorkNote.created_at.desc()).all()
    # -----------------------------------------
    
    technicians = User.query.filter_by(role='Technician').all()
    return render_template('admin/incident_detail.html', incident=incident, work_notes=work_notes, technicians=technicians)


@incidents_bp.route('/<int:id>/add_note', methods=['POST'])
@login_required
def add_work_note(id):
    """Add a new technician work note to an incident."""
    note_text = request.form.get('note')
    technician_id = current_user.id 

    if not note_text:
        flash("Work note cannot be empty.", "danger")
        return redirect(url_for('incidents.view_incident', id=id))

    new_note = WorkNote(
        # --- UPDATED: Use specific foreign key ---
        incident_id=id,
        # ---------------------------------------
        technician_id=technician_id,
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
# ... (existing code) ...
    if current_user.role != 'Admin':
        abort(403)
    incident = Incident.query.get_or_404(id)
# ... (existing code) ...
    technician_id = request.form.get('technician_id')

    if not technician_id:
        flash("Please select a technician.", "warning")
# ... (existing code) ...
        return redirect(url_for('incidents.view_incident', id=id))

    new_tech = User.query.get(technician_id)
    if not new_tech:
# ... (existing code) ...
        flash("Invalid technician selected.", "danger")
        return redirect(url_for('incidents.view_incident', id=id))

    if incident.assigned_to and incident.assigned_to != new_tech.id:
# ... (existing code) ...
        old_tech = User.query.get(incident.assigned_to)
        if old_tech and old_tech.workload > 0:
            old_tech.workload -= 1
    new_tech.workload += 1

    incident.assigned_to = new_tech.id
# ... (existing code) ...
    db.session.commit()

    flash(f"Incident reassigned to {new_tech.username}.", "success")
    return redirect(url_for('incidents.view_incident', id=id))

@incidents_bp.route('/approve/<int:id>', methods=['POST'])
@login_required
def approve_incident(id):
# ... (existing code) ...
    if current_user.role != 'Admin':
        abort(403)
    incident = Incident.query.get_or_404(id)
# ... (existing code) ...
    incident.approval_status = 'Approved'
    incident.approved_by = current_user.id
    incident.approved_at = datetime.now()
    
    technician = User.query.filter_by(role='Technician', team=incident.category)\
                         .order_by(User.workload.asc()).first()
# ... (existing code) ...
    if technician:
        incident.assigned_to = technician.id
        technician.workload += 1
    db.session.commit()

    flash(f"Incident '{incident.title}' approved successfully!", "success")
# ... (existing code) ...
    return redirect(url_for('incidents.view_incident', id=id))

@incidents_bp.route('/reject/<int:id>', methods=['POST'])
@login_required
def reject_incident(id):
# ... (existing code) ...
    if current_user.role != 'Admin':
        abort(403)
    incident = Incident.query.get_or_404(id)
# ... (existing code) ...
    incident.approval_status = 'Rejected'
    incident.approved_by = current_user.id
    incident.approved_at = datetime.now()
    db.session.commit()

    flash(f"Incident '{incident.title}' has been rejected.", "danger")
# ... (existing code) ...
    return redirect(url_for('incidents.view_incident', id=id))

