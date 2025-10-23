from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user # <-- IMPORT THESE
from models import db, Incident, ServiceRequest
from datetime import datetime

# dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/admin/dashboard')
dashboard_bp = Blueprint('dashboard', __name__)

# --- Helper function to get role-based queries ---
def get_incident_query():
    if current_user.role == 'Technician':
        # Technicians only see their own incidents
        return Incident.query.filter_by(assigned_to=current_user.id)
    else:
        # Admins see all incidents
        return Incident.query

def get_service_query():
    # For now, techs/admins see all service requests.
    # You could change this later to be team-based.
    if current_user.role == 'Technician':
        # Example: Technicians only see 'Hardware' requests if they are on that team
        # return ServiceRequest.query.filter_by(request_type=current_user.team)
        return ServiceRequest.query # Keep it simple for now
    else:
        # Admins see all
        return ServiceRequest.query

# --------------------------------------------------


@dashboard_bp.route('/')
@login_required
def dashboard_home():
    """Render dashboard page with live ticket stats + avg resolution time."""
    # Use our helper functions
    incident_q = get_incident_query()
    service_q = get_service_query()

    total_incidents = incident_q.count()
    total_services = service_q.count()

    open_tickets = incident_q.filter_by(status='Open').count() + \
                   service_q.filter_by(status='Pending').count()
    resolved_tickets = incident_q.filter_by(status='Resolved').count() + \
                       service_q.filter_by(status='Resolved').count()

    # Calculate average resolution time (this logic is now role-aware!)
    resolved_incidents = incident_q.filter_by(status='Resolved').all()
    resolved_services = service_q.filter_by(status='Resolved').all()

    total_durations = []
    for item in resolved_incidents + resolved_services:
        if item.created_at and item.updated_at:
            delta = (item.updated_at - item.created_at).total_seconds() / 3600 # hours
            total_durations.append(delta)

    if total_durations:
        avg_hours = sum(total_durations) / len(total_durations)
        if avg_hours < 1:
            avg_time = f"{int(avg_hours * 60)} min"
        else:
            avg_time = f"{round(avg_hours, 1)} hr"
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
    """Return live JSON data for charts."""
    # Use our helper functions again
    
    incident_q = get_incident_query()
    service_q = get_service_query()

    incident_statuses = ['Open', 'In Progress', 'Resolved']
    service_statuses = ['Pending', 'In Progress', 'Approved', 'Resolved']

    incident_counts = [incident_q.filter_by(status=s).count() for s in incident_statuses]
    service_counts = [service_q.filter_by(status=s).count() for s in service_statuses]

    return jsonify({
        "incident_labels": incident_statuses,
        "incident_values": incident_counts,
        "service_labels": service_statuses,
        "service_values": service_counts
    })
