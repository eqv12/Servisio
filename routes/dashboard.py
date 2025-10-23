# routes/dashboard.py

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user 
from models import db, Incident, ServiceRequest
from datetime import datetime
from sqlalchemy import or_ # <-- Import 'or_'

dashboard_bp = Blueprint('dashboard', __name__)

# --- (Helper functions are all OK) ---
def get_incident_query():
    if current_user.role == 'Technician':
        return Incident.query.filter_by(assigned_to=current_user.id)
    else:
        return Incident.query

def get_service_query():
    if current_user.role == 'Technician':
        # Now we can filter by assigned_to
        return ServiceRequest.query.filter_by(assigned_to=current_user.id)
    else:
        return ServiceRequest.query
# --------------------------------------------------

@dashboard_bp.route('/')
@login_required
def dashboard_home():
    """Render dashboard page with live ticket stats (NOW FULLY SYNCHRONIZED)."""
    incident_q = get_incident_query()
    service_q = get_service_query()

    total_incidents = incident_q.count()
    total_services = service_q.count()

    # --- ACCURATE "OPEN / PENDING" LOGIC ---
    # Count tickets that are PENDING APPROVAL
    pending_incidents = incident_q.filter_by(approval_status='Pending').count()
    pending_services = service_q.filter_by(approval_status='Pending').count()

    # Count tickets that are APPROVED and IN WORK (Open or In Progress)
    open_work_incidents = incident_q.filter(
        Incident.approval_status == 'Approved',
        Incident.status.in_(['Open', 'In Progress'])
    ).count()
    open_work_services = service_q.filter(
        ServiceRequest.approval_status == 'Approved',
        ServiceRequest.status.in_(['Open', 'In Progress'])
    ).count()

    open_tickets = pending_incidents + pending_services + open_work_incidents + open_work_services
    # -----------------------------------------------

    # --- Resolved logic ---
    resolved_tickets = incident_q.filter_by(status='Resolved').count() + \
                       service_q.filter_by(status='Resolved').count()

    # --- (Average resolution time logic) ---
    resolved_incidents_list = incident_q.filter_by(status='Resolved').all()
    resolved_services_list = service_q.filter_by(status='Resolved').all()
    
    total_durations = []
    for item in resolved_incidents_list + resolved_services_list:
        if item.created_at and item.updated_at:
            delta = (item.updated_at - item.created_at).total_seconds() / 3600
            total_durations.append(delta)

    if total_durations:
        avg_hours = sum(total_durations) / len(total_durations)
        avg_time = f"{int(avg_hours * 60)} min" if avg_hours < 1 else f"{round(avg_hours, 1)} hr"
    else:
        avg_time = "—"
    
    stats = {
        "total_tickets": total_incidents + total_services,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "avg_resolution_time": avg_time
    }

    return render_template('admin/dashboard.html', stats=stats)


@dashboard_bp.route('/data')
@login_required
def dashboard_data():
    """Return live JSON data for charts (NOW FULLY SYNCHRONIZED)."""
    incident_q = get_incident_query()
    service_q = get_service_query()

    # --- Labels for Incident Chart ---
    incident_labels = ['Pending Approval', 'Open (Approved)', 'In Progress', 'Resolved']
    incident_values = [
        incident_q.filter_by(approval_status='Pending').count(),
        incident_q.filter(Incident.approval_status == 'Approved', Incident.status == 'Open').count(),
        incident_q.filter(Incident.status == 'In Progress').count(),
        incident_q.filter(Incident.status == 'Resolved').count()
    ]

    # --- MIRRORED Labels for Service Chart ---
    service_labels = ['Pending Approval', 'Open (Approved)', 'In Progress', 'Resolved']
    service_values = [
        service_q.filter_by(approval_status='Pending').count(),
        service_q.filter(ServiceRequest.approval_status == 'Approved', ServiceRequest.status == 'Open').count(),
        service_q.filter(ServiceRequest.status == 'In Progress').count(),
        service_q.filter(ServiceRequest.status == 'Resolved').count()
    ]

    return jsonify({
        "incident_labels": incident_labels,
        "incident_values": incident_values,
        "service_labels": service_labels,
        "service_values": service_values
    })