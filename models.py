from datetime import datetime
from flask_login import UserMixin
from extensions import db, bcrypt # <-- This is the CORRECT import
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='User') 
    team = db.Column(db.String(50), nullable=True) 
    workload = db.Column(db.Integer, default=0) 
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    incidents_created = db.relationship('Incident', foreign_keys='Incident.created_by', backref='creator', lazy=True)
    incidents_assigned = db.relationship('Incident', foreign_keys='Incident.assigned_to', backref='technician', lazy=True)
    service_requests = db.relationship(
        'ServiceRequest',
        back_populates='requester',
        foreign_keys='ServiceRequest.created_by',
        lazy=True
    )

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if a provided password matches the hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        """Generates a secure token for password reset."""
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        """Verifies the reset token and returns the user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Incident(db.Model):
    __tablename__ = 'incident'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50)) 
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Open')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    kb_article_id = db.Column(db.Integer, db.ForeignKey('kb_article.id'), nullable=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    approval_status = db.Column(db.String(50), default='Pending') 
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    kb_article = db.relationship('KBArticle')
    approver = db.relationship('User', foreign_keys=[approved_by])

    # --- Corrected WorkNote Relationship ---
    work_notes = db.relationship('WorkNote', backref='incident', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='WorkNote.incident_id')
    # ---------------------------------------


class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    request_type = db.Column(db.String(50)) 
    status = db.Column(db.String(50), default='Open')
    approval_status = db.Column(db.String(50), default='Pending')
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    requester = db.relationship('User', foreign_keys=[created_by], back_populates='service_requests')
    approver = db.relationship('User', foreign_keys=[approved_by])
    technician = db.relationship('User', foreign_keys=[assigned_to])

    # --- Corrected WorkNote Relationship ---
    work_notes = db.relationship('WorkNote', backref='service_request', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='WorkNote.service_request_id')
    # ---------------------------------------


class KBArticle(db.Model):
    __tablename__ = 'kb_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False) 
    created_at = db.Column(db.DateTime, default=db.func.now())


class TicketHistory(db.Model):
    __tablename__ = 'ticket_history'
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(20)) 
    ticket_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class WorkNote(db.Model):
    __tablename__ = 'work_note'
    id = db.Column(db.Integer, primary_key=True)
    
    # --- Corrected Foreign Keys ---
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=True)
    # ------------------------------
    
    technician_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    technician = db.relationship('User')

