"""
auth.py - Authentication & Role Management Blueprint

Purpose:
    Handles user login, logout, and role-based access.

Responsibilities:
    - Login and logout routes
    - Role verification
    - Placeholder templates for login/register forms
"""

# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from services.auth_service import (
    authenticate_user,
    login_user_and_remember,
    logout_current_user,
    create_user,
    get_user_by_username,
    roles_required,
)

auth_bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")


@auth_bp.before_app_request
def ensure_db_initialized():
    if not hasattr(current_app, "extensions") or "sqlalchemy" not in current_app.extensions:
        db.init_app(current_app)
        
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in, redirect to home/dashboard
    if current_user.is_authenticated:
        flash("You're already logged in.", "info")
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        if not username or not password:
            flash("Please provide both username and password.", "danger")
            return render_template("auth/login.html", username=username)

        user = authenticate_user(username, password)
        if user:
            login_user_and_remember(user, remember=remember)
            flash("Login successful. Welcome back!", "success")
            # next param support (safe redirect)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("index"))
        else:
            flash(error or "Login failed", "danger")
            return render_template("auth/login.html", username=username)

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_current_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


# Optional register route (you may restrict to Admins in prod)
@auth_bp.route("/register", methods=["GET", "POST"])
@login_required
@roles_required("Admin")  # only Admin can create other users
def register():
    """Admin-only user creation page. For initial admin creation use CLI/script."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "User")

        if not username or not password:
            flash("username and password are required", "danger")
            return render_template("auth/register.html")

        if get_user_by_username(username):
            flash("Username already exists", "warning")
            return render_template("auth/register.html")

        try:
            create_user(username=username, password=password, email=email or None, role=role)
            flash(f"User {username} created with role {role}", "success")
            return redirect(url_for("auth.register"))
        except Exception as e:
            current_app.logger.exception("Failed to create user")
            flash(f"Error creating user: {str(e)}", "danger")
            return render_template("auth/register.html")

    return render_template("auth/register.html")
    