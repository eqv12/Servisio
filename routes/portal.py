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

from flask import Blueprint, render_template, jsonify, request

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
    """Ticket creation page (form stub)."""
    if request.method == 'POST':
        # Placeholder for saving ticket logic
        return "Ticket submitted (dummy response)"
    return render_template('portal/new_ticket.html')

@portal_bp.route('/my_tickets')
def my_tickets():
    """List user’s tickets (dummy data)."""
    dummy_tickets = [
        {"id": 101, "title": "VPN not connecting", "status": "Open"},
        {"id": 102, "title": "Email access issue", "status": "Resolved"}
    ]
    return render_template('portal/my_tickets.html', tickets=dummy_tickets)

@portal_bp.route('/kb')
def portal_kb():
    """Knowledge base listing/search (dummy data)."""
    kb_articles = [
        {"id": 1, "title": "How to reset password"},
        {"id": 2, "title": "VPN setup guide"}
    ]
    return render_template('portal/kb.html', articles=kb_articles)
