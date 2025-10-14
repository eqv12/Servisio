from flask import Flask, render_template
from flask_login import login_required, current_user
from services.auth_service import init_auth
from routes.auth import auth_bp


app = Flask(__name__)
db_path = r"C:\Users\DELL\users.db"

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

# Initialize database + login manager
init_auth(app)

# Register blueprints
app.register_blueprint(auth_bp)

# Define index route for logged-in users
@app.route("/")
@login_required
def index():
    return render_template("index.html", user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
