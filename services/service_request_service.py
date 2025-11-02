from models import db, ServiceRequest
from flask_login import current_user

def create_service(title, description, request_type, user_id):
    """
    Create a new service request. Returns (service, error_message).
    """
    # Input validation
    title = (title or '').strip()
    description = (description or '').strip()
    request_type = (request_type or '').strip()
    
    if not title:
        return None, 'Title is required.'
    if not request_type:
        return None, 'Request Type is required.'
        
    try:
        service = ServiceRequest(
            title=title,
            description=description,
            request_type=request_type,
            status='Open',
            approval_status='Pending', # Start as pending
            created_by=user_id
        )
        db.session.add(service)
        db.session.commit()
        return service, None
    except Exception as e:
        db.session.rollback()
        return None, f'Error creating request: {str(e)}'

def get_user_service_requests(user_id):
    """Get all service requests created by a specific user."""
    return ServiceRequest.query.filter_by(created_by=user_id).order_by(ServiceRequest.created_at.desc()).all()

def get_technician_service_requests(technician_id):
    """Get all service requests assigned to a specific technician."""
    return ServiceRequest.query.filter_by(assigned_to=technician_id).order_by(ServiceRequest.created_at.desc()).all()

def get_all_service_requests():
    """Get all service requests, ordered by newest first."""
    return ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
