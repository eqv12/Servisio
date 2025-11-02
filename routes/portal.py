"""
portal.py - User-Facing Portal Blueprint
...
"""

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
# --- IMPORT BOTH SERVICES ---
from services import incident_service
from services import service_request_service
from services.kb_service import get_all_articles, search_articles
from flask_login import login_required, current_user
# --- IMPORT THE NEW FORMS ---
from forms import PortalIncidentForm, PortalServiceForm


portal_bp = Blueprint('portal', __name__)

@portal_bp.route('/')
@login_required
def portal_home():
    """User dashboard with real ticket stats for the logged-in user."""
    user_id = current_user.id # Use current_user
    
    # Get stats for *both* incidents and service requests
    incidents = incident_service.get_user_incidents(user_id)
    services = service_request_service.get_user_service_requests(user_id)
    tickets = incidents + services
    
    stats = {"open": 0, "in_progress": 0, "resolved": 0}
    for t in tickets:
        # Check for 'Pending' approval OR 'Open'/'In Progress' work status
        if t.approval_status == 'Pending' or t.status in ('Open', 'In Progress'):
            stats["open"] += 1
        elif t.status == 'Resolved':
            stats["resolved"] += 1
            
    return render_template('portal/index.html', stats=stats)


@portal_bp.route('/create_incident', methods=['GET', 'POST'])
@login_required
def create_incident():
    """User-facing page to create an incident."""
    form = PortalIncidentForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.category.data
        
        # --- THIS IS THE FIX ---
        # 1. We now accept three return values
        incident, error, tech_name = incident_service.create_incident(
            title=title,
            description=description,
            category=category,
            user_id=current_user.id
            # Priority is set to 'Medium' by default in the service
        )
        # ---------------------

        if error:
            flash(error, 'danger')
        else:
            # 2. Use the new tech_name in the flash message
            flash(f"Incident created successfully! Assigned to {tech_name if tech_name else 'No available technician.'}", 'success')
            return redirect(url_for('portal.my_tickets'))
            
    return render_template('portal/create_incident.html', form=form, title="Report an Incident")


@portal_bp.route('/create_service', methods=['GET', 'POST'])
@login_required
def create_service():
    """User-facing page to create a service request."""
    form = PortalServiceForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        request_type = form.request_type.data

        # --- THIS IS THE FIX ---
        # 1. We now accept three return values
        service, error, tech_name = service_request_service.create_service(
            title=title,
            description=description,
            request_type=request_type,
            user_id=current_user.id
        )
        # ---------------------

        if error:
            flash(error, 'danger')
        else:
            # 2. Use the new tech_name in the flash message
            flash(f"Service request created successfully! Assigned to {tech_name if tech_name else 'No available technician.'}", 'success')
            return redirect(url_for('portal.my_tickets'))

    return render_template('portal/create_service.html', form=form, title="Request a Service")


@portal_bp.route('/my_tickets')
@login_required
def my_tickets():
    """List all of user's tickets (incidents AND services)."""
    user_id = current_user.id
    incidents = incident_service.get_user_incidents(user_id)
    services = service_request_service.get_user_service_requests(user_id)
    
    # Combine and sort the list by creation date
    tickets = sorted(incidents + services, key=lambda x: x.created_at, reverse=True)
    
    q = request.args.get('q', '').strip()
    if q:
        q_lower = q.lower()
        tickets = [t for t in tickets if (q_lower in (t.title or '').lower() or q_lower in (t.description or '').lower())]
        
    return render_template('portal/my_tickets.html', tickets=tickets, q=q)


@portal_bp.route('/closed_requests')
@login_required
def closed_requests():
    """List user's closed requests (status = Resolved or Rejected)."""
    user_id = current_user.id
    incidents = incident_service.get_user_incidents(user_id)
    services = service_request_service.get_user_service_requests(user_id)
    
    all_tickets = incidents + services
    closed_tickets = [
        t for t in all_tickets if (t.status == 'Resolved' or t.approval_status == 'Rejected')
    ]
    
    # Sort by update time
    closed_tickets = sorted(closed_tickets, key=lambda x: x.updated_at, reverse=True)
    
    return render_template('portal/closed_requests.html', tickets=closed_tickets)

