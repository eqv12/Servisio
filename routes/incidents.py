"""
incidents.py - Admin/Technician Incident Management Blueprint

Purpose:
    CRUD operations for incident tickets on the admin side.

Responsibilities:
    - View, add, edit, and delete incidents
    - Provide dummy data for frontend tables
"""

from flask import Blueprint, render_template, jsonify, request

incidents_bp = Blueprint('incidents', __name__)

@incidents_bp.route('/')
def list_incidents():
    """List all incidents (dummy data)."""
    dummy_incidents = [
        {"id": 1, "title": "VPN not working", "status": "Open", "priority": "High"},
        {"id": 2, "title": "Printer issue", "status": "Resolved", "priority": "Low"}
    ]
    return render_template('admin/incidents.html', incidents=dummy_incidents)

@incidents_bp.route('/<int:incident_id>')
def view_incident(incident_id):
    """View a single incident (dummy)."""
    incident = {"id": incident_id, "title": "VPN not working", "status": "Open", "priority": "High"}
    return render_template('admin/incident_detail.html', incident=incident)

@incidents_bp.route('/create', methods=['GET', 'POST'])
def create_incident():
    """Form placeholder for creating a new incident."""
    if request.method == 'POST':
        # Save logic placeholder
        return "Incident created (dummy response)"
    return render_template('admin/incident_create.html')
