"""
kb.py - Knowledge Base Blueprint

Purpose:
    CRUD and search for Knowledge Base articles.

Responsibilities:
    - Add, edit, delete KB articles
    - Return article lists and search results
    - Provide dummy data for portal/admin
"""

from flask import Blueprint, jsonify

kb_bp = Blueprint('kb', __name__)

@kb_bp.route('/')
def list_articles():
    """Return dummy KB article list"""
    return jsonify([
        {"id": 1, "title": "How to reset password", "content": "Step by step instructions..."}
    ])
