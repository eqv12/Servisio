from models import db, Incident
from flask_login import current_user

def create_incident(title, description, category, user_id, priority='Medium'):
    """
    Create a new incident ticket. Returns (incident, error_message).
    Priority is now set by default or by an admin, not the user.
    """
    # Input validation
    title = (title or '').strip()
    description = (description or '').strip()
    category = (category or '').strip()
    
    if not title:
        return None, 'Title is required.'
    if not category:
        return None, 'Category is required.'
        
    try:
        incident = Incident(
            title=title,
            description=description,
            category=category,
            priority=priority,  # Set to default 'Medium'
            status='Open',
            approval_status='Pending', # Start as pending
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

def get_technician_incidents(technician_id):
    """Get all incidents assigned to a specific technician."""
    return Incident.query.filter_by(assigned_to=technician_id).order_by(Incident.created_at.desc()).all()

def get_all_incidents():
    """Get all incidents, ordered by newest first."""
    return Incident.query.order_by(Incident.created_at.desc()).all()
