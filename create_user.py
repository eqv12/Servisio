# create_users.py

from models import db, User
from werkzeug.security import generate_password_hash
from app import create_app

app = create_app()

with app.app_context():
    # Clear existing users (optional)
    # db.drop_all()
    # db.create_all()
    db.create_all()

    users = [
        {"username": "admin", "password": "a123", "role": "admin"},
        {"username": "tech1", "password": "t123", "role": "technician"},
        {"username": "user1", "password": "u123", "role": "user"},
    ]

    for u in users:
        if not User.query.filter_by(username=u["username"]).first():
            new_user = User(
                username=u["username"],
                password=generate_password_hash(u["password"], method="pbkdf2:sha256"),
                role=u["role"]
            )
            db.session.add(new_user)

    db.session.commit()
    print("✅ Admin, Technician, and User accounts created successfully!")
