"""
portal.py - User-Facing Portal Blueprint
...
"""

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
# --- Import all services and forms ---
from services import incident_service, service_request_service, kb_service
from forms import PortalIncidentForm, PortalServiceForm
from flask_login import login_required, current_user
# -------------------------------------

portal_bp = Blueprint('portal', __name__)

@portal_bp.route('/')
@login_required
def portal_home():
    """User dashboard with real ticket stats for the logged-in user."""
    # --- FIX: Use current_user.id, not session ---
    user_id = current_user.id
    
    # --- FIX: Get both incidents and services ---
    incidents = incident_service.get_user_incidents(user_id)
    services = service_request_service.get_user_service_requests(user_id)
    all_tickets = incidents + services
    
    stats = {"open": 0, "in_progress": 0, "resolved": 0}
    for t in all_tickets:
        # Check both status and approval_status
        if t.approval_status == 'Pending':
            stats["open"] += 1
        elif t.status in ('Open', 'In Progress'):
            stats["in_progress"] += 1
        elif t.status == 'Resolved':
            stats["resolved"] += 1
            
    return render_template('portal/index.html', stats=stats)


# --- NEW: Route for creating incidents ---
@portal_bp.route('/create_incident', methods=['GET', 'POST'])
@login_required
def create_incident():
    """User-facing page to create an incident."""
    form = PortalIncidentForm()
    if form.validate_on_submit():
        incident, error = incident_service.create_incident(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            user_id=current_user.id  # <-- FIX: Use logged-in user
        )
        if error:
            flash(error, 'danger')
        else:
            flash('Incident created successfully and is pending approval!', 'success')
            return redirect(url_for('portal.my_tickets'))
            
    return render_template('portal/create_incident.html', form=form)


# --- NEW: Route for creating service requests ---
@portal_bp.route('/create_service', methods=['GET', 'POST'])
@login_required
def create_service():
    """User-facing page to create a service request."""
    form = PortalServiceForm()
    if form.validate_on_submit():
        service, error = service_request_service.create_service(
            title=form.title.data,
            description=form.description.data,
            request_type=form.request_type.data,
            user_id=current_user.id  # <-- FIX: Use logged-in user
        )
        if error:
            flash(error, 'danger')
        else:
            flash('Service request created successfully and is pending approval!', 'success')
            return redirect(url_for('portal.my_tickets'))
            
    return render_template('portal/create_service.html', form=form)


@portal_bp.route('/my_tickets')
@login_required
def my_tickets():
    """List user’s tickets (from DB), with optional search."""
    # --- FIX: Get both incidents and services ---
    user_id = current_user.id
    incidents = incident_service.get_user_incidents(user_id)
    services = service_request_service.get_user_service_requests(user_id)
    
    # Combine and sort by creation date
    all_tickets = sorted(incidents + services, key=lambda x: x.created_at, reverse=True)

    q = request.args.get('q', '').strip()
    if q:
        q_lower = q.lower()
        all_tickets = [t for t in all_tickets if (q_lower in (t.title or '').lower() or q_lower in (t.description or '').lower())]
        
    return render_template('portal/my_tickets.html', tickets=all_tickets, q=q)


@portal_bp.route('/closed_requests')
@login_required
def closed_requests():
    """List user's closed requests (status = closed)."""
    # --- FIX: Get both incidents and services ---
    user_id = current_user.id
    incidents = incident_service.get_user_incidents(user_id)
    services = service_request_service.get_user_service_requests(user_id)
    
    all_tickets = incidents + services
    closed_tickets = [t for t in all_tickets if (t.status and t.status.lower() == 'resolved')]
    
    return render_template('portal/closed_requests.html', tickets=closed_tickets)

