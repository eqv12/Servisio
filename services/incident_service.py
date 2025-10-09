from models import db, Incident

def create_incident(title, description, priority, user_id):
	"""Create a new incident ticket."""
	incident = Incident(
		title=title,
		description=description,
		priority=priority,
		created_by=user_id
	)
	db.session.add(incident)
	db.session.commit()
	return incident

def get_user_incidents(user_id):
	"""Get all incidents created by a specific user."""
	return Incident.query.filter_by(created_by=user_id).order_by(Incident.created_at.desc()).all()
