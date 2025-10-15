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
from flask_login import UserMixin
from flask_bcrypt import Bcrypt 

db = SQLAlchemy()  # Initialize in app.py after importing
bcrypt = Bcrypt()

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, raw_password: str):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password, raw_password)

    # Relationships
    incidents = db.relationship('Incident', back_populates='creator', lazy=True)
    service_requests = db.relationship('ServiceRequest', back_populates='requester', lazy=True)


class Incident(db.Model):
    __tablename__ = 'incident'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    creator = db.relationship('User', back_populates='incidents')

class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    request_type = db.Column(db.String(50))
    status = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    requester = db.relationship('User', back_populates='service_requests')



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