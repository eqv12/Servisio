from models import db, KBArticle

def get_all_articles():
	"""Return all KB articles."""
	return KBArticle.query.order_by(KBArticle.created_at.desc()).all()

def search_articles(keyword):
	"""Search KB articles by keyword in title or content."""
	if not keyword:
		return get_all_articles()
	search = f"%{keyword}%"
	return KBArticle.query.filter(
		(KBArticle.title.ilike(search)) | (KBArticle.content.ilike(search))
	).order_by(KBArticle.created_at.desc()).all()
