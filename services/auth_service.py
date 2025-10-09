# services/auth_service.py
import os
from functools import wraps

from flask import current_app, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


# ---------- Models ----------
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="User")  # Admin, Technician, User
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, raw_password: str):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    def get_role(self):
        return self.role or "User"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
        }


# ---------- Initialization ----------
def init_auth(app):
    """Initialize SQLAlchemy and LoginManager for the app."""
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # create tables if not exist (only for development)
    with app.app_context():
        if app.config.get("CREATE_DB_ON_START", True):
            db.create_all()


# ---------- CRUD + Auth helpers ----------
def create_user(username: str, password: str, email: str = None, role: str = "User"):
    if User.query.filter_by(username=username).first():
        raise ValueError("Username already exists")
    user = User(username=username, role=role)
    user.password = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_username(username: str):
    return User.query.filter_by(username=username).first()


def get_user_by_id(user_id: int):
    return User.query.get(user_id)


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return None, "User not found"
    if not check_password_hash(user.password, password):
        return None, "Invalid password"
    return user, None


def login_user_and_remember(user, remember=False):
    login_user(user, remember=remember)
    return True


def logout_current_user():
    logout_user()


# ---------- Decorators for role-based access ----------
def roles_required(*allowed_roles):
    """
    Decorator: restrict endpoint to users whose role is in allowed_roles.
    usage: @roles_required('Admin', 'Technician')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.get_role() not in allowed_roles:
                flash("You don't have permission to view that page.", "warning")
                # Redirect to a safe page (home)
                return redirect(url_for("index"))
            return fn(*args, **kwargs)
        return wrapper
    return decorator
