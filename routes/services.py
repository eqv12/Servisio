"""
services.py - Admin/Technician Service Request Management Blueprint

Purpose:
    CRUD operations for service requests.

Responsibilities:
    - View, add, edit, and delete service requests
    - Provide dummy data for frontend
"""

from flask import Blueprint, render_template, jsonify, request

services_bp = Blueprint('services', __name__)

@services_bp.route('/')
def list_services():
    """List all service requests (dummy)."""
    dummy_services = [
        {"id": 1, "title": "Request VPN access", "status": "Pending"},
        {"id": 2, "title": "Request new keyboard", "status": "Approved"}
    ]
    return render_template('admin/services.html', services=dummy_services)

@services_bp.route('/<int:service_id>')
def view_service(service_id):
    """View a specific service request (dummy)."""
    service = {"id": service_id, "title": "Request VPN access", "status": "Pending"}
    return render_template('admin/service_detail.html', service=service)
