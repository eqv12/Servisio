from threading import Thread
from flask import render_template, current_app, url_for
from flask_mail import Message
from extensions import mail

def _send_async_email(app, msg):
    """
    Helper function to send email in a background thread.
    This prevents the app from freezing while the email is sent.
    """
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            # You can add more robust logging here
            print(f"Error sending email: {e}")

def send_email(subject, recipients, template, **kwargs):
    """
    A generic function to build and send an email.
    
    :param subject: The subject line of the email.
    :param recipients: A list of email addresses.
    :param template: The .html template to use (e.g., 'email/new_user_alert.html').
    :param kwargs: The variables to pass into the template (e.g., user=user).
    """
    # Get the app instance
    app = current_app._get_current_object()
    
    # Render the HTML body from the template
    html_body = render_template(template, **kwargs)
    
    # Create the email message
    msg = Message(
        subject=subject,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=recipients,
        html=html_body
    )
    
    # Start the background thread to send it
    Thread(target=_send_async_email, args=(app, msg)).start()

# --- Specific Email Functions ---

def send_new_user_alert(admin_list, new_user):
    """
    Sends an alert to all admins about a new user pending approval.
    """
    admin_emails = [admin.email for admin in admin_list]
    subject = f"New Account Approval Required: {new_user.username}"
    
    send_email(
        subject,
        admin_emails,
        'email/new_user_alert.html',
        new_user=new_user
    )

def send_account_approved_email(user):
    """
    Sends an email to a user telling them their account is now active.
    """
    subject = "Your Servisio Account Has Been Approved!"
    
    send_email(
        subject,
        [user.email],
        'email/account_approved.html',
        user=user
    )

def send_ticket_assigned_email(technician, ticket):
    """
    Sends an email to a technician about a new ticket.
    """
    ticket_type = "Incident" if hasattr(ticket, 'priority') else "Service Request"
    subject = f"New Ticket Assignment: {ticket_type} #{ticket.id}"
    
    send_email(
        subject,
        [technician.email],
        'email/assignment.html',
        technician=technician,
        ticket=ticket,
        ticket_type=ticket_type
    )

# --- NEW FUNCTION FOR PASSWORD RESET ---
def send_password_reset_email(user):
    """
    Generates a token and sends the password reset email.
    """
    token = user.get_reset_token()
    # _external=True is crucial to generate a full URL (http://...)
    reset_link = url_for('auth.reset_token', token=token, _external=True)
    
    subject = "Servisio Password Reset Request"
    
    send_email(
        subject,
        [user.email],
        'email/reset_password.html',
        user=user,
        reset_link=reset_link
    )

