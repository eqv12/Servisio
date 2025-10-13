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
from datetime import datetime, timedelta
import random

app = create_app()
app.app_context().push()

# Drop and recreate tables (optional for fresh start)
db.drop_all()
db.create_all()

# --- Users ---
random.seed(42)

first_names = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Sam",
    "Avery", "Quinn", "Drew", "Kai"
]
roles = ["Admin", "Technician", "User", "User", "User"]

users = []
for idx, name in enumerate(first_names, start=1):
    role = roles[0] if idx == 1 else (roles[1] if idx in (2, 3) else random.choice(roles[2:]))
    username = name.lower() + str(idx)
    email = f"{username}@servisio.com"
    password = ("admin123" if role == "Admin" else ("tech123" if role == "Technician" else "user123"))
    users.append(User(username=username, email=email, password=password, role=role))

db.session.add_all(users)
db.session.commit()

user_ids = [u.id for u in users]
technician_ids = [u.id for u in users if u.role == "Technician"]


# --- Incidents ---
incident_titles = [
    "VPN not connecting",
    "Printer not responding",
    "Email not syncing",
    "Blue screen on startup",
    "Wi-Fi drops intermittently",
    "Software crash on launch",
    "Unable to access shared drive",
    "Slow computer performance",
    "Headset not detected",
    "Remote desktop not working",
    "Projector not displaying",
    "Two-factor code not received",
    "Frequent application freezes",
    "USB ports not functioning",
    "Keyboard keys stuck",
    "Mouse lagging",
    "Website blocked unexpectedly",
    "Outlook calendar not updating",
    "Microphone not working",
    "Display flickering",
    "Disk space low warning",
    "Battery drains quickly",
    "Cannot print double-sided",
    "Audio output not switching",
    "Clipboard not syncing"
]

incident_statuses = ["Open", "In Progress", "Resolved", "Closed"]
priorities = ["Low", "Medium", "High"]

now = datetime.utcnow()
incidents = []
for i in range(30):
    title = random.choice(incident_titles)
    created_by = random.choice(user_ids)
    priority = random.choices(priorities, weights=[0.3, 0.5, 0.2])[0]
    status = random.choices(incident_statuses, weights=[0.35, 0.35, 0.2, 0.1])[0]
    created_offset_days = random.randint(0, 45)
    created_at = now - timedelta(days=created_offset_days, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    # If resolved/closed, set updated_at after created_at by 1–72 hours; else set recent update
    if status in ("Resolved", "Closed"):
        hours_to_resolve = random.randint(1, 72)
        updated_at = created_at + timedelta(hours=hours_to_resolve, minutes=random.randint(0, 59))
    else:
        updated_at = created_at + timedelta(hours=random.randint(0, 24), minutes=random.randint(0, 59))

    incidents.append(Incident(
        title=title,
        description=f"{title} observed by user. Needs investigation.",
        status=status,
        priority=priority,
        created_by=created_by,
        created_at=created_at,
        updated_at=updated_at
    ))

db.session.add_all(incidents)
db.session.commit()

# --- Service Requests ---
sr_titles = [
    "Request new mouse",
    "Request software installation",
    "New laptop request",
    "Extra monitor setup",
    "Access to finance folder",
    "Create email distribution list",
    "VPN access request",
    "Install Adobe Acrobat",
    "Upgrade to Windows 11",
    "Request for admin rights",
    "New account creation",
    "Password reset",
    "Provision virtual machine",
    "Request new headset",
    "Install Python environment",
    "Install Node.js",
    "Shared mailbox access",
    "Jira project access",
    "Slack channel creation",
    "Request docking station"
]
sr_statuses = ["Pending", "Approved", "Completed", "Rejected"]
sr_types = ["Hardware", "Software", "Network", "Access", "Accounts"]

services = []
for i in range(30):
    title = random.choice(sr_titles)
    created_by = random.choice(user_ids)
    request_type = random.choices(sr_types, weights=[0.35, 0.35, 0.15, 0.1, 0.05])[0]
    status = random.choices(sr_statuses, weights=[0.4, 0.25, 0.3, 0.05])[0]
    created_offset_days = random.randint(0, 45)
    created_at = now - timedelta(days=created_offset_days, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    updated_at = created_at + timedelta(hours=random.randint(1, 48))
    services.append(ServiceRequest(
        title=title,
        description=f"{title} submitted by user for fulfillment.",
        status=status,
        request_type=request_type,
        created_by=created_by,
        created_at=created_at,
        updated_at=updated_at
    ))

db.session.add_all(services)
db.session.commit()

# --- Knowledge Base Articles ---
kb_items = [
    ("Resetting VPN Connection", "Steps to reconnect VPN...", "Network"),
    ("Fixing Printer Jam", "How to resolve printer issues...", "Hardware"),
    ("Installing Software", "Procedure for new installations...", "Software"),
    ("Password Reset Guide", "Steps to reset your password...", "Accounts"),
    ("Troubleshooting Wi-Fi", "Improve Wi-Fi connectivity and reduce drops.", "Network"),
    ("Outlook Tips", "Managing calendar sync and shared mailboxes.", "Software"),
    ("Laptop Care", "Best practices to extend laptop battery life.", "Hardware"),
    ("Using VPN Securely", "Security tips for remote access.", "Network"),
    ("OneDrive Sync Issues", "Resolve common sync conflicts.", "Software"),
    ("Access Request Process", "How to request folder/application access.", "Access"),
    ("Printer Setup", "Add network printers on Windows and macOS.", "Hardware"),
    ("Teams Audio Setup", "Configure mic/headset for calls.", "Software"),
    ("Remote Desktop", "Connecting to on-prem resources.", "Network"),
    ("Updating Windows", "Keeping Windows up to date.", "Software"),
    ("Email Best Practices", "Avoiding phishing and spam.", "Accounts"),
    ("Secure Passwords", "Creating and storing strong passwords.", "Accounts"),
    ("Shared Drive Mapping", "Map network drives via VPN.", "Network"),
    ("Audio Troubleshooting", "Fixing no-audio or low volume.", "Hardware"),
    ("Monitor Calibration", "Adjust brightness and color.", "Hardware"),
    ("Software Request Policy", "Approved software catalog and process.", "Software")
]
articles = [KBArticle(title=t, content=c, category=cat) for (t, c, cat) in kb_items]
db.session.add_all(articles)
db.session.commit()


print("✅ Database seeded successfully with dummy data!")
