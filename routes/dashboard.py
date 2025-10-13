from flask import Blueprint, render_template, jsonify
from models import db, Incident, ServiceRequest
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/admin/dashboard')


@dashboard_bp.route('/')
def dashboard_home():
    """Render dashboard page with live ticket stats + avg resolution time."""
    total_incidents = Incident.query.count()
    total_services = ServiceRequest.query.count()

    open_tickets = Incident.query.filter_by(status='Open').count() + ServiceRequest.query.filter_by(status='Pending').count()
    resolved_tickets = Incident.query.filter_by(status='Resolved').count() + ServiceRequest.query.filter_by(status='Resolved').count()

    # Calculate average resolution time for resolved tickets
    resolved_incidents = Incident.query.filter_by(status='Resolved').all()
    resolved_services = ServiceRequest.query.filter_by(status='Resolved').all()

    total_durations = []
    for item in resolved_incidents + resolved_services:
        if item.created_at and item.updated_at:
            delta = (item.updated_at - item.created_at).total_seconds() / 3600  # hours
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
def dashboard_data():
    """Return live JSON data for charts."""
    incident_statuses = ['Open', 'In Progress', 'Resolved']
    service_statuses = ['Pending', 'In Progress', 'Approved', 'Resolved']

    incident_counts = [Incident.query.filter_by(status=s).count() for s in incident_statuses]
    service_counts = [ServiceRequest.query.filter_by(status=s).count() for s in service_statuses]

    return jsonify({
        "incident_labels": incident_statuses,
        "incident_values": incident_counts,
        "service_labels": service_statuses,
        "service_values": service_counts
    })
