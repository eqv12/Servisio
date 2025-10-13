"""
api.py - Shared / External API Blueprint

Purpose:
    Placeholder for APIs used by frontend or external services.

Responsibilities:
    - Provide endpoints for integrations
    - Return dummy JSON for parallel frontend dev
"""

from flask import Blueprint, jsonify, request
from utils.chatbot import ask_chatbot

api_bp = Blueprint('api', __name__)

@api_bp.route('/status')
def api_status():
    """Return API status"""
    return jsonify({"status": "API running"})


@api_bp.route('/chatbot', methods=['POST'])
def api_chatbot():
    """Chatbot endpoint: expects JSON {"message": "..."} and returns {"reply": "..."}."""
    try:
        data = request.get_json(silent=True) or {}
        message = (data.get('message') or '').strip()
        if not message:
            return jsonify({"error": "Missing 'message'"}), 400

        reply = ask_chatbot(message)
        return jsonify({"reply": reply})
    except Exception as exc:
        # Avoid leaking internals to clients
        return jsonify({"error": "Chatbot service unavailable"}), 500
