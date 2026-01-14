"""
Email utilities for sending notifications
"""
import os
import traceback
from typing import Optional, Tuple
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import execute_query


def get_admin_email() -> str:
    """Get admin email from database or environment variable"""
    try:
        # Get admin email from environment variable first
        admin_email_env = os.getenv("ADMIN_EMAIL")
        if admin_email_env:
            # Try to find this email in database
            users = execute_query("SELECT email FROM users WHERE email = %s AND role = 'admin' AND is_active = 1 LIMIT 1", 
                                 (admin_email_env,))
            if users and len(users) > 0:
                admin_email = users[0]['email']
                print(f"[EMAIL] Found admin email in database: {admin_email}")
                return admin_email
            # If not in database, use the env value
            print(f"[EMAIL] Using admin email from environment: {admin_email_env}")
            return admin_email_env
    except Exception as e:
        print(f"Error getting admin email from database: {str(e)}")
    
    # Fallback: Get from environment variable (required)
    admin_email = os.getenv("ADMIN_EMAIL")
    if not admin_email:
        raise ValueError("ADMIN_EMAIL environment variable is required. Set it in .env file or cPanel environment variables.")
    
    print(f"[EMAIL] Using admin email from environment: {admin_email}")
    return admin_email


def send_email_sync(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None,
    sender_email: Optional[str] = None
) -> bool:
    """
    Send email notification using SMTP (synchronous)
    Returns True if email was sent successfully, False otherwise
    """
    try:
        # Get SMTP settings from environment variables (all required)
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port_str = os.getenv("SMTP_PORT", "587")
        smtp_port = int(smtp_port_str) if smtp_port_str else 587
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        # Validate required SMTP settings
        if not smtp_host:
            print("[EMAIL ERROR] SMTP_HOST environment variable not set.")
            return False
        if not smtp_user:
            print("[EMAIL ERROR] SMTP_USER environment variable not set.")
            return False
        if not smtp_password:
            print("[EMAIL ERROR] SMTP_PASSWORD environment variable not set.")
            return False
        
        # Sender email (can be different from SMTP username)
        if sender_email is None:
            sender_email = os.getenv("SMTP_SENDER")
            if not sender_email:
                sender_email = get_admin_email()
        
        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = subject
        
        # Add plain text and HTML parts
        text_part = MIMEText(body, "plain")
        message.attach(text_part)
        
        if html_body:
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
        
        # Send email using smtplib (synchronous)
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)
        
        print(f"[EMAIL SUCCESS] Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {str(e)}")
        traceback.print_exc()
        return False


def parse_visit_details_from_message(message: str) -> Tuple[Optional[str], Optional[str], str]:
    """Parse visit date and time from the message. Returns (visit_date, visit_time, additional_notes)"""
    visit_date = None
    visit_time = None
    additional_notes = message
    
    try:
        if "Preferred Date:" in message:
            lines = message.split('\n')
            for i, line in enumerate(lines):
                if "Preferred Date:" in line:
                    date_part = line.split("Preferred Date:")[-1].strip()
                    if date_part:
                        visit_date = date_part
                
                if "Preferred Time:" in line:
                    time_part = line.split("Preferred Time:")[-1].strip()
                    if time_part:
                        visit_time = time_part
                
                if "Additional Notes:" in line:
                    additional_notes = '\n'.join(lines[i+1:]).strip()
                    break
    except Exception as e:
        print(f"Error parsing visit details: {str(e)}")
    
    return visit_date, visit_time, additional_notes


def send_schedule_visit_email(
    visitor_name: str,
    visitor_email: str,
    visitor_phone: Optional[str],
    visit_date: Optional[str],
    visit_time: Optional[str],
    message: str,
    property_id: Optional[int] = None
) -> bool:
    """Send email notification to admin about a new Schedule Visit request"""
    try:
        admin_email = get_admin_email()
        
        # Get property details if property_id is provided
        property_title = ""
        property_location = ""
        if property_id:
            try:
                # Check residential_properties first
                properties = execute_query("SELECT property_name as title, CONCAT(city, ', ', locality) as location FROM residential_properties WHERE id = %s", (property_id,))
                if not properties or len(properties) == 0:
                    # Check plot_properties if not found in residential
                    properties = execute_query("SELECT project_name as title, CONCAT(city, ', ', locality) as location FROM plot_properties WHERE id = %s", (property_id,))
                if properties and len(properties) > 0:
                    prop = properties[0]
                    property_title = prop['title']
                    property_location = prop['location']
            except Exception as e:
                print(f"Error fetching property details: {str(e)}")
        
        subject = f"New Schedule Visit Request - {visitor_name}"
        
        property_info = ""
        if property_title:
            property_info = f"\nProperty: {property_title}\nLocation: {property_location}\n"
        
        body = f"""New Schedule Visit Request Received

Visitor Details:
- Name: {visitor_name}
- Email: {visitor_email}
- Phone: {visitor_phone or 'Not provided'}
{property_info}Visit Details:
- Preferred Date: {visit_date or 'Not specified'}
- Preferred Time: {visit_time or 'Not specified'}

Message:
{message}

---
This is an automated notification from Tirumakudalu Properties.
Please log in to the dashboard to view and manage this request.
"""
        
        property_html = ""
        if property_title:
            property_html = f'<p><strong>Property:</strong> {property_title}</p><p><strong>Location:</strong> {property_location}</p>'
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2c3e50;">New Schedule Visit Request Received</h2>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #2c3e50;">Visitor Details:</h3>
                <p><strong>Name:</strong> {visitor_name}</p>
                <p><strong>Email:</strong> <a href="mailto:{visitor_email}">{visitor_email}</a></p>
                <p><strong>Phone:</strong> {visitor_phone or 'Not provided'}</p>
                {property_html}
            </div>
            <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #2c3e50;">Visit Details:</h3>
                <p><strong>Preferred Date:</strong> {visit_date or 'Not specified'}</p>
                <p><strong>Preferred Time:</strong> {visit_time or 'Not specified'}</p>
            </div>
            <div style="background-color: #fff; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #2c3e50;">Message:</h3>
                <p style="white-space: pre-wrap;">{message}</p>
            </div>
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            <p style="color: #7f8c8d; font-size: 12px;">
                This is an automated notification from Tirumakudalu Properties.<br>
                Please log in to the dashboard to view and manage this request.
            </p>
        </body>
        </html>
        """
        
        return send_email_sync(admin_email, subject, body, html_body)
        
    except Exception as e:
        print(f"[EMAIL ERROR] Error in send_schedule_visit_email: {str(e)}")
        traceback.print_exc()
        return False


def send_self_notification_email(
    notification_type: str,
    title: str,
    message: str,
    details: Optional[dict] = None
) -> bool:
    """Send a self-reminder email to the admin about site notifications."""
    try:
        admin_email = get_admin_email()
        
        subject = f"🔔 Site Notification Reminder: {title}"
        
        details_text = ""
        details_html = ""
        if details:
            details_text = "\n\nAdditional Details:\n"
            details_html = '<div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;"><h3 style="margin-top: 0; color: #2c3e50;">Additional Details:</h3>'
            for key, value in details.items():
                if value is not None:
                    key_formatted = key.replace('_', ' ').title()
                    details_text += f"- {key_formatted}: {value}\n"
                    details_html += f'<p><strong>{key_formatted}:</strong> {value}</p>'
            details_html += "</div>"
        
        body = f"""Site Notification Reminder

{title}

{message}
{details_text}
---
This is an automated reminder from Tirumakudalu Properties.
Please log in to your dashboard to view and manage this notification.
"""
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="background-color: #3498db; color: white; padding: 20px; border-radius: 5px 5px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">🔔 Site Notification Reminder</h1>
            </div>
            <div style="padding: 20px; background-color: #fff;">
                <h2 style="color: #2c3e50; margin-top: 0;">{title}</h2>
                <div style="background-color: #fff; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0;">
                    <p style="white-space: pre-wrap; margin: 0;">{message}</p>
                </div>
                {details_html}
                <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center;">
                    <p style="margin: 0;"><strong>Action Required:</strong> Please check your dashboard for more details.</p>
                </div>
            </div>
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            <p style="color: #7f8c8d; font-size: 12px; text-align: center;">
                This is an automated reminder from Tirumakudalu Properties.<br>
                Please log in to your dashboard to view and manage this notification.
            </p>
        </body>
        </html>
        """
        
        return send_email_sync(admin_email, subject, body, html_body, sender_email=admin_email)
        
    except Exception as e:
        print(f"[SELF-NOTIFICATION ERROR] Error in send_self_notification_email: {str(e)}")
        traceback.print_exc()
        return False
