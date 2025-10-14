# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.auth_service import (
    authenticate_user,
    login_user_and_remember,
    logout_current_user,
    create_user,
    get_user_by_username,
    roles_required
)

auth_bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")

# ---------------- Login ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Already logged in.", "info")
        return redirect(url_for("index"))  # Redirect to index instead of login

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        if not username or not password:
            flash("Provide both username and password.", "danger")
            return render_template("auth/login.html", username=username)

        user, error = authenticate_user(username, password)
        if user:
            login_user_and_remember(user, remember=remember)
            flash("Login successful.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))  # Redirect to index
        else:
            flash(error, "danger")

    return render_template("auth/login.html")


# ---------------- Logout ----------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_current_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))


# ---------------- Register (Admin Only) ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
# @login_required
# @roles_required("Admin")
def register():
    if request.method == "POST":
        print("register entered")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        role = request.form.get("role") or "User"

        if get_user_by_username(username):
            flash("Username already exists", "warning")
            return render_template("auth/register.html")

        create_user(username=username, password=password, email=email, role=role)
        flash(f"User {username} created with role {role}", "success")
        return redirect(url_for("auth.register"))

    return render_template("auth/register.html")


# ---------------- Simple Index Route ----------------
from flask import Flask

app = Flask(__name__)

@app.route("/")
@login_required
def index():
    # A simple dashboard or homepage after login
    return render_template("index.html", user=current_user)
