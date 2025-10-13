"""
analytics.py - Analytics Helper Utilities

Purpose:
    Compute and return data for Servisio dashboard and reports using real DB queries.

Responsibilities:
    - Aggregate ticket metrics from `Incident` and `ServiceRequest`
    - Calculate SLA compliance using a simple, priority-based target
    - Provide summary stats for dashboard charts
"""

from datetime import datetime
from typing import Dict, List

from models import db, Incident, ServiceRequest


# Consider these statuses as terminal/resolved
RESOLVED_STATUSES = {"Resolved", "Closed"}
# Consider these as open/in-progress
OPEN_STATUSES = {"Open", "Pending", "In Progress"}

# Simple SLA target (hours) by priority
SLA_TARGET_HOURS_BY_PRIORITY = {
    "High": 4,
    "Medium": 24,
    "Low": 72,
}


def _format_duration_human(total_seconds: float) -> str:
    minutes = int(total_seconds // 60)
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours}h {minutes}m"


def _incident_duration_seconds(incident: Incident, now: datetime) -> float:
    start = incident.created_at or now
    # If resolved/closed, use updated_at as resolution time; else use now
    if (incident.status or "").strip() in RESOLVED_STATUSES and incident.updated_at:
        end = incident.updated_at
    else:
        end = now
    return max(0.0, (end - start).total_seconds())


def _is_sla_breach(incident: Incident, now: datetime) -> bool:
    priority = (incident.priority or "").strip().capitalize()
    target_hours = SLA_TARGET_HOURS_BY_PRIORITY.get(priority, 24)
    duration_seconds = _incident_duration_seconds(incident, now)
    return duration_seconds > target_hours * 3600


def get_ticket_summary() -> Dict[str, object]:
    """Return real ticket summary metrics for dashboard."""
    now = datetime.utcnow()

    total_tickets = db.session.query(Incident.id).count()

    open_tickets = (
        db.session.query(Incident.id)
        .filter(Incident.status.in_(tuple(OPEN_STATUSES)))
        .count()
    )

    resolved_tickets = (
        db.session.query(Incident.id)
        .filter(Incident.status.in_(tuple(RESOLVED_STATUSES)))
        .count()
    )

    # Average resolution time for resolved incidents
    resolved_incidents: List[Incident] = (
        Incident.query.filter(Incident.status.in_(tuple(RESOLVED_STATUSES))).all()
    )
    if resolved_incidents:
        total_resolve_seconds = sum(_incident_duration_seconds(i, now) for i in resolved_incidents)
        avg_resolve_seconds = total_resolve_seconds / max(1, len(resolved_incidents))
        avg_resolution_time = _format_duration_human(avg_resolve_seconds)
    else:
        avg_resolution_time = "0h 0m"

    # SLA breaches on incidents using simple priority-based target
    all_incidents: List[Incident] = Incident.query.all()
    sla_breaches = sum(1 for i in all_incidents if _is_sla_breach(i, now))

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "avg_resolution_time": avg_resolution_time,
        "sla_breaches": sla_breaches,
    }


def get_tickets_by_category() -> Dict[str, List]:
    """Return distribution of Service Requests by `request_type` as labels/values."""
    # Aggregate counts by request_type (non-null/non-empty)
    rows = (
        db.session.query(ServiceRequest.request_type, db.func.count(ServiceRequest.id))
        .filter(db.func.trim(db.func.coalesce(ServiceRequest.request_type, "")) != "")
        .group_by(ServiceRequest.request_type)
        .order_by(ServiceRequest.request_type.asc())
        .all()
    )
    labels = [r[0] for r in rows]
    values = [int(r[1]) for r in rows]
    return {"labels": labels, "values": values}


def get_sla_compliance() -> int:
    """Return SLA compliance percentage across all incidents (0-100)."""
    now = datetime.utcnow()
    total = db.session.query(Incident.id).count()
    if total == 0:
        return 100
    incidents = Incident.query.all()
    breaches = sum(1 for i in incidents if _is_sla_breach(i, now))
    compliance = int(round(100 * (total - breaches) / total))
    return max(0, min(100, compliance))
