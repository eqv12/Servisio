from models import db, Incident

def create_incident(title, description, priority, user_id):
	"""Create a new incident ticket. Returns (incident, error_message)."""
	# Input validation
	title = (title or '').strip()
	description = (description or '').strip()
	priority = (priority or '').strip().capitalize()
	if not title:
		return None, 'Title is required.'
	if not priority:
		return None, 'Priority is required.'
	if priority not in ['Low', 'Medium', 'High']:
		return None, 'Priority must be Low, Medium, or High.'
	try:
		incident = Incident(
			title=title,
			description=description,
			priority=priority,
			status='Open',
			created_by=user_id
		)
		db.session.add(incident)
		db.session.commit()
		return incident, None
	except Exception as e:
		db.session.rollback()
		return None, f'Error creating ticket: {str(e)}'

def get_user_incidents(user_id):
	"""Get all incidents created by a specific user."""
	return Incident.query.filter_by(created_by=user_id).order_by(Incident.created_at.desc()).all()
