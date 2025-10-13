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

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Incident, WorkNote, User
from datetime import datetime

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



@incidents_bp.route('/create', methods=['GET', 'POST'])
def create_incident():
    """Create a new incident"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')

        if not title or not description:
            flash("Title and description are required.", "danger")
            return redirect(url_for('incidents.create_incident'))

        new_incident = Incident(
            title=title,
            description=description,
            priority=priority,
            status='Open',
            created_by=1  # temporary: assume Admin ID=1
        )

        db.session.add(new_incident)
        db.session.commit()
        flash("Incident created successfully!", "success")
        return redirect(url_for('incidents.list_incidents'))

    return render_template('admin/incident_create.html')




"""
Developer Notes:
----------------
- Uses simple form POST → DB insert → redirect to list page.
- Later you’ll replace created_by=1 with current_user.id after auth setup.
- Requires a template: templates/admin/incident_create.html
"""
@incidents_bp.route('/update/<int:id>', methods=['POST'])
def update_incident(id):
    """Update an incident's status"""
    incident = Incident.query.get_or_404(id)
    new_status = request.form.get('status')

    if new_status and new_status != incident.status:
        incident.status = new_status
        db.session.commit()
        flash(f"Incident #{id} updated to '{new_status}'.", "success")

    return redirect(url_for('incidents.list_incidents'))


"""
Developer Notes:
----------------
- Each row in incidents.html includes a <form> that triggers this route.
- The 'onchange' event automatically submits the form when status changes.
- Later you can add role-based logic to restrict updates to admins/techs.
"""
@incidents_bp.route('/delete/<int:id>', methods=['POST'])
def delete_incident(id):
    """Delete an incident by ID"""
    incident = Incident.query.get(id)
    if incident:
        db.session.delete(incident)
        db.session.commit()
        flash(f"Incident #{id} deleted successfully.", "success")
    else:
        flash("Incident not found.", "danger")

    return redirect(url_for('incidents.list_incidents'))

"""
Developer Notes:
----------------
- Incident model fields expected: id, title, description, status, priority, created_at, created_by
- Add guards in template for optional fields (e.g., created_by might be None)
- This file now returns real DB data (no dummy lists)
"""

@incidents_bp.route('/<int:id>')
def view_incident(id):
    """Detailed view of an incident with work notes."""
    incident = Incident.query.get_or_404(id)
    work_notes = WorkNote.query.filter_by(incident_id=id).order_by(WorkNote.created_at.desc()).all()
    technicians = User.query.filter_by(role='Technician').all()
    return render_template('admin/incident_detail.html', incident=incident, work_notes=work_notes, technicians=technicians)


@incidents_bp.route('/<int:id>/add_note', methods=['POST'])
def add_work_note(id):
    """Add a new technician work note to an incident."""
    note_text = request.form.get('note')
    technician_id = request.form.get('technician_id') or 2  # placeholder; integrate with login later

    if not note_text:
        flash("Work note cannot be empty.", "danger")
        return redirect(url_for('incidents.view_incident', id=id))

    new_note = WorkNote(
        incident_id=id,
        technician_id=technician_id,
        note=note_text,
        created_at=datetime.now()
    )
    db.session.add(new_note)
    db.session.commit()
    flash("Work note added successfully!", "success")
    return redirect(url_for('incidents.view_incident', id=id))
