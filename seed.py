"""
seed.py - Dummy Data Seeder for Servisio

Purpose:
    Populates the database with sample users, incidents,
    service requests, and knowledge base articles.

Usage:
    Run once after creating the database:
        python seed.py
"""

from app import create_app
from models import db, User, Incident, ServiceRequest, KBArticle
from datetime import datetime

app = create_app()
app.app_context().push()

# Drop and recreate tables (optional for fresh start)
db.drop_all()
db.create_all()

# --- Users ---
users = [
    User(username="admin", password="admin123", role="Admin"),
    User(username="tech1", password="tech123", role="Technician"),
    User(username="tech2", password="tech123", role="Technician"),
    User(username="user1", password="user123", role="User"),
    User(username="user2", password="user123", role="User"),
]
db.session.add_all(users)
db.session.commit()

# --- Incidents ---
incidents = [
    Incident(title="VPN not connecting", description="Cannot connect to office VPN.",
             status="Open", priority="High", created_by=4),
    Incident(title="Printer not responding", description="Printer in Room 204 is offline.",
             status="Resolved", priority="Medium", created_by=5),
    Incident(title="Email not syncing", description="Outlook not fetching new emails.",
             status="In Progress", priority="High", created_by=4),
]
db.session.add_all(incidents)
db.session.commit()

# --- Service Requests ---
services = [
    ServiceRequest(title="Request new mouse", description="Mouse not working properly.",
                   status="Pending", created_by=5),
    ServiceRequest(title="Request software installation", description="Need MS Project installed.",
                   status="Approved", created_by=4)
]
db.session.add_all(services)
db.session.commit()

# --- Knowledge Base Articles ---
articles = [
    KBArticle(title="How to reset your password",
              content="1. Go to account settings...\n2. Click 'Reset Password'..."),
    KBArticle(title="How to connect to VPN",
              content="1. Open VPN client...\n2. Enter credentials...\n3. Click Connect.")
]
db.session.add_all(articles)
db.session.commit()

print("✅ Database seeded successfully with dummy data!")
