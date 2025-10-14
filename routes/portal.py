"""
portal.py - User-Facing Portal Blueprint

Purpose:
    Serves all user-side (employee) views for Servisio.
    Allows users to raise tickets, track status, and access knowledge base.

Responsibilities:
    - /portal            → user dashboard
    - /portal/new_ticket → create new incident/service request
    - /portal/my_tickets → list of user-created tickets
    - /portal/kb         → knowledge base search/view
"""

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session, flash
from services.incident_service import create_incident, get_user_incidents
from services.kb_service import get_all_articles, search_articles

portal_bp = Blueprint('portal', __name__)

@portal_bp.route('/')
def portal_home():
    """User dashboard with real ticket stats for the logged-in user."""
    user_id = session.get('user_id', 1)  # Replace with real session user_id
    tickets = get_user_incidents(user_id)
    stats = {"open": 0, "in_progress": 0, "resolved": 0}
    for t in tickets:
        status = t.status.lower() if t.status else ''
        if status == 'open':
            stats["open"] += 1
        elif status in ('in progress', 'in_progress'):
            stats["in_progress"] += 1
        elif status == 'resolved':
            stats["resolved"] += 1
    return render_template('portal/index.html', stats=stats)

@portal_bp.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    """Ticket creation page (real DB logic, robust)."""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        user_id = session.get('user_id', 1)
        incident, error = create_incident(title, description, priority, user_id)
        if error:
            flash(error, 'danger')
            return render_template('portal/new_ticket.html', title=title, description=description, priority=priority)
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('portal.my_tickets'))
    return render_template('portal/new_ticket.html')

@portal_bp.route('/my_tickets')
def my_tickets():
    """List user’s tickets (from DB), with optional search."""
    user_id = session.get('user_id', 1)
    tickets = get_user_incidents(user_id)
    q = request.args.get('q', '').strip()
    if q:
        q_lower = q.lower()
        tickets = [t for t in tickets if (q_lower in (t.title or '').lower() or q_lower in (t.description or '').lower())]
    return render_template('portal/my_tickets.html', tickets=tickets, q=q)

@portal_bp.route('/closed_requests')
def closed_requests():
    """List user's closed requests (status = closed)."""
    user_id = session.get('user_id', 1)
    tickets = get_user_incidents(user_id)
    closed_tickets = [t for t in tickets if (t.status and t.status.lower() == 'closed')]
    return render_template('portal/closed_requests.html', tickets=closed_tickets)