# services/auth_service.py
from functools import wraps
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


# ---------- Models ----------
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="User")  # Admin, Technician, User
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, raw_password: str):
        self.password = raw_password

    def check_password(self, raw_password: str) -> bool:
        return self.password == raw_password

    def get_role(self):
        return self.role or "User"

    def has_role(self, *roles):
        return self.get_role() in roles

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
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    with app.app_context():
        if app.config.get("CREATE_DB_ON_START", True):
            db.create_all()


# ---------- CRUD + Auth Helpers ----------
def create_user(username: str, password: str, email: str = None, role: str = "User"):
    if User.query.filter_by(username=username).first():
        raise ValueError("Username already exists")
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_username(username: str):
    return User.query.filter_by(username=username).first()


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return None, "User not found"
    if not user.check_password(password):
        return None, "Invalid password"
    return user, None


def login_user_and_remember(user, remember=False):
    login_user(user, remember=remember)
    return True


def logout_current_user():
    logout_user()


# ---------- Decorators ----------
def roles_required(*roles):
    """Decorator for role-based access on Flask routes."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(*roles):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator