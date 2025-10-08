"""
api.py - Shared / External API Blueprint

Purpose:
    Placeholder for APIs used by frontend or external services.

Responsibilities:
    - Provide endpoints for integrations
    - Return dummy JSON for parallel frontend dev
"""

from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/status')
def api_status():
    """Return API status"""
    return jsonify({"status": "API running"})
