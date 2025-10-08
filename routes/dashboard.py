"""
dashboard.py - Admin Dashboard Blueprint

Purpose:
    Provide analytics and summaries for administrators.

Responsibilities:
    - Return JSON for dashboard charts
    - Render admin dashboard page using dummy metrics
"""

from flask import Blueprint, render_template, jsonify

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard_home():
    """Render admin dashboard with dummy stats."""
    stats = {
        "total_tickets": 10,
        "open_tickets": 4,
        "resolved_tickets": 6,
        "avg_resolution_time": "2h 30m"
    }
    return render_template('admin/dashboard.html', stats=stats)

@dashboard_bp.route('/data')
def dashboard_data():
    """Return dummy JSON for Chart.js graphs."""
    chart_data = {
        "labels": ["Open", "In Progress", "Resolved"],
        "values": [4, 2, 6]
    }
    return jsonify(chart_data)
