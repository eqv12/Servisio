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

from datetime import datetime
from flask_login import UserMixin  # <-- IMPORT THIS
from extensions import db, bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    
    # --- VITAL CHANGE ---
    # Rename 'password' to 'password_hash' for clarity and security
    password_hash = db.Column(db.String(128), nullable=False)
    # --------------------
    
    role = db.Column(db.String(20), nullable=False, default='User') 
    team = db.Column(db.String(50), nullable=True) 
    workload = db.Column(db.Integer, default=0) 

    # Relationships
    incidents_created = db.relationship('Incident', foreign_keys='Incident.created_by', backref='creator', lazy=True)
    incidents_assigned = db.relationship('Incident', foreign_keys='Incident.assigned_to', backref='technician', lazy=True)
    service_requests = db.relationship(
        'ServiceRequest',
        back_populates='requester',
        foreign_keys='ServiceRequest.created_by',
        lazy=True
    )

    # --- ADD THESE HELPER METHODS ---
    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if a provided password matches the hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    # --------------------------------

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
