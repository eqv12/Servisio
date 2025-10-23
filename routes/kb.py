# routes/kb.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import services.kb_service as kb_service
from forms import ArticleForm, KBSearchForm

kb_bp = Blueprint('kb', __name__)

@kb_bp.route('/')
@login_required
def kb_home():
    """
    Shows the Knowledge Base home page with categories and a search bar.
    This is the page you wanted.
    """
    search_form = KBSearchForm()
    # Get categories from the service
    categories = kb_service.get_categories()
    
    # If no articles, provide some defaults for the cards
    if not categories:
        categories = ['Hardware', 'Software', 'Network']
        
    return render_template('kb/home.html', categories=categories, search_form=search_form)

@kb_bp.route('/search')
@login_required
def search_results():
    """Displays search results from the KB."""
    query = request.args.get('query', '')
    if not query:
        return redirect(url_for('kb.kb_home'))
        
    articles = kb_service.search_articles(query)
    return render_template('kb/list.html', articles=articles, title=f"Search results for '{query}'")

@kb_bp.route('/category/<string:category_name>')
@login_required
def view_category(category_name):
    """Displays all articles in a specific category."""
    articles = kb_service.get_articles_by_category(category_name)
    return render_template('kb/list.html', articles=articles, title=f"Category: {category_name}")

@kb_bp.route('/article/<int:article_id>')
@login_required
def view_article(article_id):
    """Displays a single KB article."""
    article = kb_service.get_article_by_id(article_id)
    return render_template('kb/view.html', article=article)

@kb_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_article():
    """
    Page for creating a new KB article.
    Only accessible to Admins and Technicians.
    """
    # Protect the route
    if current_user.role not in ('Admin', 'Technician'):
        flash('You do not have permission to create articles.', 'danger')
        return redirect(url_for('kb.kb_home'))

    form = ArticleForm()
    # Get unique categories from DB to populate the dropdown
    form.category.choices = [(cat, cat) for cat in kb_service.get_categories()]
    # Add common defaults if they don't exist
    for default in ['Hardware', 'Software', 'Network', 'Other']:
        if (default, default) not in form.category.choices:
            form.category.choices.append((default, default))

    if form.validate_on_submit():
        article, error = kb_service.create_article(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data
        )
        if error:
            flash(f'Error creating article: {error}', 'danger')
        else:
            flash('Article created successfully!', 'success')
            return redirect(url_for('kb.view_article', article_id=article.id))
            
    return render_template('kb/create.html', title='Create Article', form=form)

@kb_bp.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    """
    Page for editing an existing KB article.
    Only accessible to Admins and Technicians.
    """
    # Protect the route
    if current_user.role not in ('Admin', 'Technician'):
        flash('You do not have permission to edit articles.', 'danger')
        return redirect(url_for('kb.kb_home'))

    article = kb_service.get_article_by_id(article_id)
    # Pass `obj=article` to pre-populate the form with the article's data
    form = ArticleForm(obj=article) 
    
    # Dynamically populate categories just like in create_article
    form.category.choices = [(cat, cat) for cat in kb_service.get_categories()]
    for default in ['Hardware', 'Software', 'Network', 'Other']:
        if (default, default) not in form.category.choices:
            form.category.choices.append((default, default))

    if form.validate_on_submit():
        # This runs on POST
        updated_article, error = kb_service.update_article(
            article_id=article_id,
            title=form.title.data,
            content=form.content.data,
            category=form.category.data
        )
        if error:
            flash(f'Error updating article: {error}', 'danger')
        else:
            flash('Article updated successfully!', 'success')
            return redirect(url_for('kb.view_article', article_id=updated_article.id))
            
    # This runs on GET (showing the pre-filled form)
    return render_template('kb/edit.html', title='Edit Article', form=form, article=article)