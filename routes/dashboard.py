"""
routes/dashboard.py
-------------------
Admin / Technician Dashboard Module

Purpose:
    Displays live analytics and key metrics for incidents and service requests.
    Provides a JSON endpoint for charts (used by Chart.js on the frontend).
"""

from flask import Blueprint, render_template, jsonify
from models import db, Incident, ServiceRequest

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/admin/dashboard')


@dashboard_bp.route('/')
def dashboard_home():
    """Render dashboard page with live ticket stats."""
    total_incidents = Incident.query.count()
    total_services = ServiceRequest.query.count()

    open_tickets = Incident.query.filter_by(status='Open').count() + ServiceRequest.query.filter_by(status='Pending').count()
    resolved_tickets = Incident.query.filter_by(status='Resolved').count() + ServiceRequest.query.filter_by(status='Resolved').count()

    stats = {
        "total_tickets": total_incidents + total_services,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "avg_resolution_time": "2h 30m (static placeholder)"
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


"""
Developer Notes:
----------------
- The /admin/dashboard route renders the HTML page with summary cards.
- The /admin/dashboard/data route supplies JSON to Chart.js for live charts.
- Later you can compute real avg resolution time or add SLAs easily.
"""
