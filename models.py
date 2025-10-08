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
    """User table with roles."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    tickets = db.relationship('Incident', backref='creator', lazy=True)

class Incident(db.Model):
    """Incident tickets table."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Open')
    priority = db.Column(db.String(20), default='Medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class ServiceRequest(db.Model):
    """Service requests table."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class KBArticle(db.Model):
    """Knowledge Base articles."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TicketHistory(db.Model):
    """History of ticket updates."""
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(20))  # Incident / ServiceRequest
    ticket_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
