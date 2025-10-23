# services/kb_service.py

from models import db, KBArticle
from sqlalchemy import or_
# Add these to the top of services/kb_service.py
import google.generativeai as genai
from flask import current_app

def get_all_articles():
    """Fetches all KB articles, ordered by title."""
    return KBArticle.query.order_by(KBArticle.title).all()

def get_article_by_id(article_id):
    """Fetches a single KB article by its ID."""
    return KBArticle.query.get_or_404(article_id)

def search_articles(query):
    """Searches for articles where the query matches title or content."""
    search_term = f"%{query}%"
    return KBArticle.query.filter(
        or_(
            KBArticle.title.ilike(search_term),
            KBArticle.content.ilike(search_term)
        )
    ).all()

def get_articles_by_category(category):
    """Fetches all articles belonging to a specific category."""
    return KBArticle.query.filter_by(category=category).order_by(KBArticle.title).all()

def create_article(title, content, category):
    """Creates and saves a new KB article."""
    try:
        article = KBArticle(
            title=title,
            content=content,
            category=category
        )
        db.session.add(article)
        db.session.commit()
        return article, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def get_categories():
    """Gets a unique, sorted list of all categories."""
    # This query efficiently gets unique categories from the DB
    categories = db.session.query(KBArticle.category).distinct().order_by(KBArticle.category).all()
    # categories will be a list of tuples, e.g., [('Hardware',), ('Network',)]
    # We convert it to a simple list: ['Hardware', 'Network']
    return [category[0] for category in categories]

def update_article(article_id, title, content, category):
    """Updates an existing KB article."""
    try:
        article = get_article_by_id(article_id) # Reuse your existing function
        if not article:
            return None, "Article not found."

        article.title = title
        article.content = content
        article.category = category
        
        db.session.commit()
        return article, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)
    
# Add this new function to the end of services/kb_service.py
def get_rag_response(user_query: str) -> str:
    """
    Gets a response from the Gemini model using RAG.
    """
    # --- Step 1: Configure the API ---
    # Safely get the API key from the current Flask app's configuration
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key:
        return "Error: GEMINI_API_KEY is not configured. Please set it in your .env file."
    
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        # This can happen if the API key is invalid
        return f"Error configuring the AI service: {e}"

    # --- Step 2: Retrieve - Search your local knowledge base ---
    # We reuse your existing search function to find relevant articles
    relevant_articles = search_articles(user_query)

    # --- Step 3: Augment - Build the context for the AI ---
    context = "No relevant information found in the knowledge base."
    if relevant_articles:
        context = "Based on the Servisio knowledge base, here is some relevant information:\n\n"
        # Combine the content of the top 3 most relevant articles
        for article in relevant_articles[:3]:
            context += f"--- Article: {article.title} ---\n"
            context += f"{article.content}\n\n"

    # --- Step 4: Generate - Create the prompt and call the AI ---
    # This is the prompt template. We instruct the AI on how to behave.
    prompt_template = f"""
    You are "Servisio Guide", a helpful AI assistant for the Servisio ITSM tool.
    Your role is to answer user questions based ONLY on the provided context from the knowledge base.
    If the context does not contain the answer, you must state that you do not have that information.
    Do not make up answers or provide information from outside the given context.
    
    CONTEXT:
    {context}
    
    QUESTION:
    {user_query}
    
    ANSWER:
    """

    try:
        # Initialize the model and generate the response
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt_template)
        return response.text
    except Exception as e:
        # Handle potential API errors (e.g., quota exceeded, server issues)
        return f"An error occurred while communicating with the AI service: {e}"