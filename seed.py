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
    User(username="admin", email="admin@servisio.com", password="admin123", role="Admin"),
    User(username="tech1", email="tech1@servisio.com", password="tech123", role="Technician"),
    User(username="tech2", email="tech2@servisio.com", password="tech123", role="Technician"),
    User(username="user1", email="user1@servisio.com", password="user123", role="User"),
    User(username="user2", email="user2@servisio.com", password="user123", role="User"),
]
db.session.add_all(users)
db.session.commit()

# Convenient references
admin = users[0]
tech1 = users[1]
tech2 = users[2]
user1 = users[3]
user2 = users[4]

# --- Incidents ---
incidents = [
    Incident(
        title="VPN not connecting",
        description="Cannot connect to office VPN.",
        status="Open",
        priority="High",
        created_by=user1.id
    ),
    Incident(
        title="Printer not responding",
        description="Printer in Room 204 is offline.",
        status="Resolved",
        priority="Medium",
        created_by=user2.id
    ),
    Incident(
        title="Email not syncing",
        description="Outlook not fetching new emails.",
        status="In Progress",
        priority="High",
        created_by=user1.id
    ),
]
db.session.add_all(incidents)
db.session.commit()

# --- Service Requests ---
services = [
    ServiceRequest(
        title="Request new mouse",
        description="Mouse not working properly.",
        status="Pending",
        request_type="Hardware",
        created_by=user2.id
    ),
    ServiceRequest(
        title="Request software installation",
        description="Need MS Project installed.",
        status="Approved",
        request_type="Software",
        created_by=user1.id
    )
]
db.session.add_all(services)
db.session.commit()

# --- Knowledge Base Articles ---

articles = [
    KBArticle(title="Resetting VPN Connection", content="Steps to reconnect VPN...", category="Network"),
    KBArticle(title="Fixing Printer Jam", content="How to resolve printer issues...", category="Hardware"),
    KBArticle(title="Installing Software", content="Procedure for new installations...", category="Software"),
    KBArticle(title="Password Reset Guide", content="Steps to reset your password...", category="Accounts"),
]
db.session.add_all(articles)
db.session.commit()


print("✅ Database seeded successfully with dummy data!")
