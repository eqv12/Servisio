"""
analytics.py - Analytics Helper Utilities

Purpose:
    Compute and return data for Servisio dashboard and reports.

Responsibilities:
    - Aggregate ticket metrics
    - Calculate SLA compliance (dummy data for now)
    - Provide summary stats for dashboard charts
"""

from random import randint

def get_ticket_summary():
    """
    Returns dummy ticket summary data for dashboard.
    """
    return {
        "total_tickets": 25,
        "open_tickets": 7,
        "resolved_tickets": 15,
        "avg_resolution_time": "3h 15m",
        "sla_breaches": 3
    }

def get_tickets_by_category():
    """
    Returns dummy distribution of tickets by category.
    """
    return {
        "labels": ["Network", "Hardware", "Software", "Access"],
        "values": [5, 8, 7, 5]
    }

def get_sla_compliance():
    """
    Returns dummy SLA compliance rate.
    """
    return randint(85, 100)
