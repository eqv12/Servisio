"""
sla.py - SLA (Service Level Agreement) Utilities

Purpose:
    Provides helper functions for SLA calculation and breach detection.

Responsibilities:
    - Track SLA timers per ticket
    - Identify tickets exceeding SLA limits
    - Provide dummy responses for testing
"""

from datetime import datetime, timedelta

def get_sla_deadline(priority: str) -> datetime:
    """
    Returns SLA deadline timestamp based on ticket priority.
    
    Args:
        priority (str): Ticket priority level (Low, Medium, High)
    
    Returns:
        datetime: Deadline for SLA.
    """
    now = datetime.utcnow()
    if priority == "High":
        return now + timedelta(hours=4)
    elif priority == "Medium":
        return now + timedelta(hours=12)
    return now + timedelta(hours=24)

def is_sla_breached(created_at: datetime, priority: str) -> bool:
    """
    Checks if SLA has been breached for a given ticket.
    """
    return datetime.utcnow() > get_sla_deadline(priority)

def get_dummy_sla_data():
    """
    Returns sample SLA metrics for dashboard analytics.
    """
    return {
        "total_tickets": 25,
        "breached_tickets": 3,
        "sla_compliance_rate": "88%"
    }
