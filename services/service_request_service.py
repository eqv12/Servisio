from models import db, ServiceRequest, User
from flask_login import current_user
from services.email_service import send_ticket_assigned_email
from sqlalchemy import func
import random

def _auto_assign_technician(category):
    """
    Finds the best technician for a new ticket.
    (This is a simpler, more robust version)
    
    UPDATED: This function now ignores teams and assigns to ANY
    active technician with the lowest workload.
    """
    try:
        # 1. Get all *active* technicians
        all_active_techs = User.query.filter_by(
            role='Technician',
            is_active=True
        ).all()

        # 2. If no techs are found, return None
        if not all_active_techs:
            print(f"Auto-assign Warning: No active technicians found in the system.")
            return None

        # 3. Find the minimum workload among them
        min_workload = min(tech.workload for tech in all_active_techs)
        
        # 4. Get a list of all techs who have that minimum workload
        best_technicians = [
            tech for tech in all_active_techs 
            if tech.workload == min_workload
        ]

        # 5. Pick one at random from the "best" list
        if best_technicians:
            return random.choice(best_technicians)
        
        return None
    except Exception as e:
        print(f"Error in auto-assign: {e}")
        return None

def create_service(title, description, request_type, user_id):
    """
    Create a new service request, auto-assign it, and send an email.
    """
    title = (title or '').strip()
    description = (description or '').strip()
    request_type = (request_type or '').strip()
    
    if not title:
        return None, 'Title is required.', None
    if not request_type:
        return None, 'Request Type is required.', None
        
    try:
        service = ServiceRequest(
            title=title,
            description=description,
            request_type=request_type,
            status='Open',
            approval_status='Pending',
            created_by=user_id
        )

        # Pass the request_type, but the function will ignore it
        technician = _auto_assign_technician(request_type) 
        if technician:
            service.assigned_to = technician.id
            technician.workload += 1
        else:
            print(f"Assign. Info: Service Request (unassigned). No active technician found.")
            
        db.session.add(service)
        db.session.commit()
        
        if technician:
            send_ticket_assigned_email(technician, service)
            
        return service, None, (technician.username if technician else None)

    except Exception as e:
        db.session.rollback()
        return None, f'Error creating request: {str(e)}', None

def get_user_service_requests(user_id):
    """Get all service requests created by a specific user."""
    return ServiceRequest.query.filter_by(created_by=user_id).order_by(ServiceRequest.created_at.desc()).all()

def get_technician_service_requests(technician_id):
    """Get all service requests assigned to a specific technician."""
    return ServiceRequest.query.filter_by(assigned_to=technician_id).order_by(ServiceRequest.created_at.desc()).all()

def get_all_service_requests():
    """Get all service requests, ordered by newest first."""
    return ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()

