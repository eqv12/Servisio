"""
models.py - Database Models

Purpose:
    Define all database tables and relationships for SmartITSM.

Responsibilities:
    - User, Incident, ServiceRequest, KBArticle, TicketHistory tables
    - Define fields, data types, relationships
    - Provide basic helper methods (optional) for dummy data

Usage:
    Import models in routes for CRUD operations.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # Initialize in app.py after importing

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='User')  # Admin / Manager / Technician / User
    team = db.Column(db.String(50), nullable=True)  # e.g., Network, Hardware, Software
    workload = db.Column(db.Integer, default=0)  # number of assigned open tickets

    # Relationships
    incidents_created = db.relationship('Incident', foreign_keys='Incident.created_by', backref='creator', lazy=True)
    incidents_assigned = db.relationship('Incident', foreign_keys='Incident.assigned_to', backref='technician', lazy=True)
    service_requests = db.relationship(
    'ServiceRequest',
    back_populates='requester',
    foreign_keys='ServiceRequest.created_by',
    lazy=True
)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Incident(db.Model):
    __tablename__ = 'incident'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # Network, Hardware, Software, etc.
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Open')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    kb_article_id = db.Column(db.Integer, db.ForeignKey('kb_article.id'), nullable=True)

    # 👇 New fields
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    approval_status = db.Column(db.String(50), default='Pending')  # Pending / Approved / Rejected

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    kb_article = db.relationship('KBArticle')

    # Relationships
    approver = db.relationship('User', foreign_keys=[approved_by])



class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    request_type = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Pending Approval')  # default status
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    requester = db.relationship('User', foreign_keys=[created_by], back_populates='service_requests')
    approver = db.relationship('User', foreign_keys=[approved_by])





class KBArticle(db.Model):
    __tablename__ = 'kb_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # e.g. "Network", "Hardware", "Software"
    created_at = db.Column(db.DateTime, default=db.func.now())



class TicketHistory(db.Model):
    """History of ticket updates."""
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(20))  # Incident / ServiceRequest
    ticket_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class WorkNote(db.Model):
    __tablename__ = 'work_note'
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))
    technician_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Relationships
    incident = db.relationship('Incident', backref='work_notes')
    technician = db.relationship('User')
