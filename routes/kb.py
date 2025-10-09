from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, KBArticle

kb_bp = Blueprint('kb', __name__, url_prefix='/kb')


@kb_bp.route('/')
def kb_home():
    """KB Home - shows categories of articles."""
    categories = db.session.query(KBArticle.category).distinct().all()
    categories = [c[0] for c in categories]  # unpack from tuples
    return render_template('kb/home.html', categories=categories)


@kb_bp.route('/category/<string:category>')
def kb_by_category(category):
    """Display articles filtered by category."""
    query = request.args.get('q', '').strip()

    if query:
        articles = KBArticle.query.filter(
            (KBArticle.category == category) &
            ((KBArticle.title.ilike(f"%{query}%")) | (KBArticle.content.ilike(f"%{query}%")))
        ).order_by(KBArticle.created_at.desc()).all()
        flash(f"Results for '{query}' in {category}", "info")
    else:
        articles = KBArticle.query.filter_by(category=category).order_by(KBArticle.created_at.desc()).all()

    return render_template('kb/list.html', articles=articles, query=query, category=category)


@kb_bp.route('/<int:id>')
def view_article(id):
    article = KBArticle.query.get_or_404(id)
    return render_template('kb/view.html', article=article)


@kb_bp.route('/create', methods=['GET', 'POST'])
def create_article():
    """Create a new KB article."""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')

        if not title or not content or not category:
            flash("All fields are required.", "danger")
            return redirect(url_for('kb.create_article'))

        new_article = KBArticle(title=title, content=content, category=category)
        db.session.add(new_article)
        db.session.commit()
        flash("Article created successfully!", "success")
        return redirect(url_for('kb.kb_home'))

    categories = ['Network', 'Hardware', 'Software', 'Accounts', 'Other']
    return render_template('kb/create.html', categories=categories)


@kb_bp.route('/delete/<int:id>', methods=['POST'])
def delete_article(id):
    article = KBArticle.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash("Article deleted successfully!", "success")
    return redirect(url_for('kb.kb_home'))


from flask import jsonify

@kb_bp.route('/api/search')
def kb_api_search():
    """
    API endpoint for chatbot or AJAX integrations.
    Accepts ?q= keyword and optional ?category= filters.
    Returns JSON with article summaries.
    """
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    if not query and not category:
        return jsonify({"error": "Please provide a search query or category."}), 400

    q = KBArticle.query

    if category:
        q = q.filter_by(category=category)

    if query:
        q = q.filter(
            (KBArticle.title.ilike(f"%{query}%")) |
            (KBArticle.content.ilike(f"%{query}%"))
        )

    results = q.order_by(KBArticle.created_at.desc()).limit(10).all()

    data = [
        {
            "id": a.id,
            "title": a.title,
            "category": a.category,
            "snippet": (a.content[:150] + "...") if len(a.content) > 150 else a.content,
            "created_at": a.created_at.strftime('%Y-%m-%d'),
            "url": url_for('kb.view_article', id=a.id, _external=True)
        }
        for a in results
    ]

    return jsonify({"count": len(data), "results": data})
