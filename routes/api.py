from flask import Blueprint, request, jsonify
from services.kb_service import get_rag_response # <-- IMPORT the new function

# Create a Blueprint for API routes
api_bp = Blueprint(
    'api_bp', __name__,
    url_prefix='/api'
)

@api_bp.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint to handle chat messages from the user.
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    user_message = data.get('message')

    # Call our RAG function to get a real response from Gemini!
    bot_reply = get_rag_response(user_message)
    
    # Return the bot's reply as JSON
    return jsonify({"reply": bot_reply})