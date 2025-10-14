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


@api_bp.route('/test-kb')
def test_kb():
    """Test endpoint to verify knowledge base articles are available"""
    try:
        from models import KBArticle
        articles = KBArticle.query.all()
        return jsonify({
            "status": "success",
            "article_count": len(articles),
            "articles": [{
                "id": article.id,
                "title": article.title,
                "category": article.category
            } for article in articles[:5]]  # Show first 5 articles
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


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


@api_bp.route('/suggest-articles', methods=['POST'])
def suggest_articles():
    """Analyze incident title using Gemini and return relevant KB articles."""
    try:
        data = request.get_json(silent=True) or {}
        title = (data.get('title') or '').strip()
        if not title:
            return jsonify({"error": "Missing 'title'"}), 400

        # Get all KB articles
        from models import KBArticle
        articles = KBArticle.query.all()
        
        if not articles:
            return jsonify({"suggestions": [], "message": "No knowledge base articles available"})

        # Create context for Gemini - limit to avoid token limits
        kb_context = "\n".join([
            f"ID: {article.id} | Title: {article.title} | Category: {article.category} | Content: {article.content[:150]}..."
            for article in articles[:20]  # Limit to first 20 articles to avoid token limits
        ])

        # Use Gemini to find relevant articles
        from google import genai
        client = genai.Client(api_key="AIzaSyDXx788ps8Ze3mnB7i7nqK8go6HFNDDta8")
        
        prompt = f"""You are an IT support assistant. Given an incident title, find the most relevant knowledge base articles.

Incident Title: "{title}"

Available Knowledge Base Articles:
{kb_context}

Analyze the incident title and return ONLY the article IDs (comma-separated) of the 3 most relevant articles that could help resolve this incident.
Return format: 1,5,12 (just the numbers, no other text)"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt]
        )
        
        # Parse the response to get article IDs
        suggested_ids = []
        try:
            ids_text = response.text.strip()
            # Extract numbers from the response
            import re
            numbers = re.findall(r'\d+', ids_text)
            suggested_ids = [int(num) for num in numbers[:3]]  # Take first 3 numbers
        except Exception as parse_error:
            print(f"[API] Error parsing Gemini response: {parse_error}")
            # Fallback: return first 3 articles if parsing fails
            suggested_ids = [article.id for article in articles[:3]]
        
        # Get the suggested articles with full details
        suggested_articles = []
        for article_id in suggested_ids:
            article = KBArticle.query.get(article_id)
            if article:
                suggested_articles.append({
                    "id": article.id,
                    "title": article.title,
                    "category": article.category,
                    "snippet": article.content[:200] + "..." if len(article.content) > 200 else article.content,
                    "url": f"/kb/{article.id}"
                })
        
        # If no valid articles found, return some fallback articles
        if not suggested_articles and articles:
            fallback_articles = articles[:3]
            suggested_articles = [{
                "id": article.id,
                "title": article.title,
                "category": article.category,
                "snippet": article.content[:200] + "..." if len(article.content) > 200 else article.content,
                "url": f"/kb/{article.id}"
            } for article in fallback_articles]
        
        return jsonify({"suggestions": suggested_articles})
        
    except Exception as e:
        print(f"[API] Error in suggest_articles: {e}")
        # Return fallback articles if available
        try:
            from models import KBArticle
            fallback_articles = KBArticle.query.limit(3).all()
            if fallback_articles:
                suggestions = [{
                    "id": article.id,
                    "title": article.title,
                    "category": article.category,
                    "snippet": article.content[:200] + "..." if len(article.content) > 200 else article.content,
                    "url": f"/kb/{article.id}"
                } for article in fallback_articles]
                return jsonify({"suggestions": suggestions, "fallback": True})
        except:
            pass
        return jsonify({"error": "Unable to suggest articles"}), 500