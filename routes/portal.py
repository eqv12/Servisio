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
    """User dashboard with overview counts (dummy data)."""
    stats = {
        "open": 2,
        "in_progress": 1,
        "resolved": 3
    }
    return render_template('portal/index.html', stats=stats)

@portal_bp.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    """Ticket creation page (real DB logic)."""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        # TODO: Replace with real user_id from session after login integration
        user_id = session.get('user_id', 1)  # Default to 1 for now
        if not title or not priority:
            flash('Title and Priority are required.', 'danger')
            return render_template('portal/new_ticket.html')
        create_incident(title, description, priority, user_id)
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('portal.my_tickets'))
    return render_template('portal/new_ticket.html')

@portal_bp.route('/my_tickets')
def my_tickets():
    """List user’s tickets (from DB)."""
    # TODO: Replace with real user_id from session after login integration
    user_id = session.get('user_id', 1)  # Default to 1 for now
    tickets = get_user_incidents(user_id)
    return render_template('portal/my_tickets.html', tickets=tickets)

@portal_bp.route('/kb', methods=['GET', 'POST'])
def portal_kb():
    """Knowledge base listing/search (DB)."""
    keyword = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        articles = search_articles(keyword)
    else:
        articles = get_all_articles()
    return render_template('portal/kb.html', articles=articles, keyword=keyword)
