"""
Flask Application for Tirumakudalu Properties
Main API server with all endpoints
"""

from flask import Flask, request, jsonify, send_file, abort, make_response
from flask_cors import CORS
from typing import List, Optional, Tuple
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
# In production (cPanel), environment variables are set in cPanel settings
# Get the project root directory (parent of Backend directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    # Try loading from current directory as fallback
    load_dotenv()

import base64
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import io
import json
import traceback
import threading
import time
import psutil
import platform
import os

from database import (
    init_db_pool, close_db_pool, get_db_cursor,
    test_connection, execute_query, execute_update, execute_insert
)
from pydantic import ValidationError
from schemas import (
    # Common
    MessageResponse, ErrorResponse, PaginationParams, PaginatedResponse,
    # Properties
    PropertyCreateSchema, PropertyUpdateSchema, PropertyResponseSchema,
    PropertyListResponseSchema, PropertyFilterSchema,
    # Partners
    PartnerCreateSchema, PartnerUpdateSchema, PartnerResponseSchema,
    # Testimonials
    TestimonialCreateSchema, TestimonialUpdateSchema, TestimonialResponseSchema,
    TestimonialPublicSchema,
    # Contact Inquiries
    ContactInquiryCreateSchema, ContactInquiryUpdateSchema, ContactInquiryResponseSchema,
    # Statistics
    PropertyStatsSchema, DashboardStatsSchema, FrontendStatsSchema,
    # Search
    SearchQuerySchema, SearchResponseSchema,
    # Authentication
    LoginSchema, LoginResponseSchema,
    # Visitor Info
    VisitorInfoCreateSchema, VisitorInfoResponseSchema,
    # Logs
    LogCreateSchema, LogResponseSchema,
    # Blogs
    BlogCreateSchema, BlogUpdateSchema, BlogResponseSchema,
    # System Metrics
    SystemMetricsCreateSchema, SystemMetricsResponseSchema, SystemMetricsListResponseSchema,
    # Temporary Metrics
    TemporaryMetricsCreateSchema, TemporaryMetricsResponseSchema, TemporaryMetricsCurrentResponseSchema,
    # Cache Logs
    CacheLogCreateSchema, CacheLogResponseSchema, CacheLogListResponseSchema, CacheLogFilterSchema
)
from models import PropertyType, PropertyStatus, InquiryStatus, CacheOperation, CacheStatus
from passlib.context import CryptContext
import warnings
import logging
from contextlib import redirect_stderr

# Suppress bcrypt version warning and passlib warnings
warnings.filterwarnings("ignore", category=UserWarning, module="passlib")
warnings.filterwarnings("ignore", message=".*bcrypt.*")
logging.getLogger("passlib").setLevel(logging.ERROR)

# Suppress the trapped bcrypt error by temporarily redirecting stderr during initialization
_stderr_buffer = io.StringIO()
with redirect_stderr(_stderr_buffer):
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    except Exception:
        pwd_context = CryptContext(schemes=["bcrypt"])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


# ============================================
# EMAIL UTILITIES
# ============================================

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


# ============================================
# SETUP FUNCTIONS
# ============================================

def setup_admin_user():
    """Create or update admin user with hashed password"""
    try:
        # Create users table
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(255),
                role VARCHAR(50) DEFAULT 'admin' CHECK (role IN ('admin', 'user')),
                is_active TINYINT(1) DEFAULT 1,
                last_login TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """
        try:
            execute_update(create_table_query)
        except Exception as e:
            print(f"Note: Users table creation: {str(e)}")
        
        # Create visitor_info table
        create_visitor_table_query = """
            CREATE TABLE IF NOT EXISTS visitor_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                looking_for TEXT,
                ip_address VARCHAR(45),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        try:
            execute_update(create_visitor_table_query)
            print("✓ Visitor info table created/verified")
        except Exception as e:
            print(f"Note: Visitor info table creation: {str(e)}")
        
        # Create logs table
        create_logs_table_query = """
            CREATE TABLE IF NOT EXISTS logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                log_type VARCHAR(50) NOT NULL,
                action VARCHAR(100) NOT NULL,
                description TEXT,
                user_email VARCHAR(255),
                ip_address VARCHAR(45),
                user_agent TEXT,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_log_type (log_type),
                INDEX idx_created_at (created_at),
                INDEX idx_action (action)
            )
        """
        try:
            execute_update(create_logs_table_query)
            print("✓ Logs table created/verified")
        except Exception as e:
            print(f"Note: Logs table creation: {str(e)}")
        
        # Create blogs table
        create_blogs_table_query = """
            CREATE TABLE IF NOT EXISTS blogs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                excerpt TEXT,
                content LONGTEXT,
                category VARCHAR(100),
                tags JSON,
                image_url LONGTEXT,
                author VARCHAR(255) DEFAULT 'Tirumakudalu Properties',
                views INT DEFAULT 0,
                is_featured TINYINT(1) DEFAULT 0,
                is_active TINYINT(1) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_is_active (is_active),
                INDEX idx_is_featured (is_featured),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_blogs_table_query)
            print("✓ Blogs table created/verified")
        except Exception as e:
            print(f"Note: Blogs table creation: {str(e)}")
        
        # Create system_metrics table (permanent storage for graphs)
        create_system_metrics_table_query = """
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'RAM usage percentage',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Total RAM in MB',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Total bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_system_metrics_table_query)
            print("✓ System metrics table created/verified")
        except Exception as e:
            print(f"Note: System metrics table creation: {str(e)}")
        
        # Create temporary_metrics table (temporary storage for stat cards)
        create_temp_metrics_table_query = """
            CREATE TABLE IF NOT EXISTS temporary_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'RAM usage percentage',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Total RAM in MB',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Total bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_temp_metrics_table_query)
            print("✓ Temporary metrics table created/verified")
        except Exception as e:
            print(f"Note: Temporary metrics table creation: {str(e)}")
        
        # Get admin credentials from environment
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")
        
        if not email:
            print("Warning: ADMIN_EMAIL not set. Skipping admin user setup.")
            return
        
        if not password:
            print("Warning: ADMIN_PASSWORD not set. Skipping admin user setup.")
            return
        
        password_hash = get_password_hash(password)
        
        users = execute_query("SELECT id FROM users WHERE email = %s", (email,))
        
        if users and len(users) > 0:
            update_query = "UPDATE users SET password_hash = %s, is_active = 1 WHERE email = %s"
            execute_update(update_query, (password_hash, email))
            print(f"✓ Admin user updated: {email}")
        else:
            insert_query = "INSERT INTO users (email, password_hash, full_name, role, is_active) VALUES (%s, %s, %s, %s, %s)"
            execute_update(insert_query, (email, password_hash, "Admin User", "admin", True))
            print(f"✓ Admin user created: {email}")
        
        print(f"  Admin user configured - Email: {email}")
    except Exception as e:
        print(f"Error setting up admin user: {str(e)}")


# ============================================
# FLASK APP INITIALIZATION
# ============================================

# Get debug mode from environment (default to False for production)
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"

app = Flask(__name__)

# Configure CORS
# SECURITY: In production, explicitly set ALLOWED_ORIGINS to your frontend domain(s)
# Example: ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins_str == "*":
    if not DEBUG_MODE:
        # In production, if "*" is set, warn but allow (some setups need this)
        # For better security, explicitly set ALLOWED_ORIGINS to your domain(s)
        print("WARNING: CORS is set to allow all origins. For production, set ALLOWED_ORIGINS to specific domains.")
        allowed_origins = ["*"]  # Changed: Allow in production if explicitly set to "*"
    else:
        allowed_origins = ["*"]
else:
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

CORS(app, 
     origins=allowed_origins if allowed_origins else [],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-Admin-Email"])

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_client_ip():
    """
    Get the client's real IP address, handling proxy/load balancer scenarios.
    Checks X-Forwarded-For, X-Real-IP headers, and falls back to request.remote_addr.
    This is important for cPanel/production environments behind proxies.
    """
    # Check X-Forwarded-For header (most common proxy header)
    # Format: "client_ip, proxy1_ip, proxy2_ip, ..."
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        # Get the first IP (the original client)
        client_ip = forwarded_for.split(',')[0].strip()
        if client_ip:
            return client_ip
    
    # Check X-Real-IP header (alternative proxy header)
    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip.strip()
    
    # Fallback to request.remote_addr
    return request.remote_addr or None

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Handle case-insensitive directory name (frontend vs Frontend)
FRONTEND_DIR = None
for dir_name in ["frontend", "Frontend", "FRONTEND"]:
    potential_dir = BASE_DIR / dir_name
    if potential_dir.exists() and potential_dir.is_dir():
        FRONTEND_DIR = potential_dir
        break

if FRONTEND_DIR is None:
    FRONTEND_DIR = BASE_DIR / "frontend"
    if not FRONTEND_DIR.exists():
        print(f"WARNING: Frontend directory not found at {FRONTEND_DIR}. Static file serving may be limited.")
    else:
        print(f"INFO: Using frontend directory: {FRONTEND_DIR}")

# Initialize database on app startup
print("Starting Tirumakudalu Properties API...")
if init_db_pool():
    if test_connection():
        print("Database connection successful!")
        setup_admin_user()
        # Create application_metrics table if it doesn't exist
        try:
            create_app_metrics_table = """
                CREATE TABLE IF NOT EXISTS application_metrics (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    endpoint VARCHAR(255) NOT NULL COMMENT 'API endpoint path',
                    method VARCHAR(10) NOT NULL COMMENT 'HTTP method',
                    response_time_ms DECIMAL(10, 2) NOT NULL COMMENT 'Response time in milliseconds',
                    status_code INT NOT NULL COMMENT 'HTTP status code',
                    is_error BOOLEAN DEFAULT FALSE COMMENT 'Whether the request resulted in an error',
                    ip_address VARCHAR(45) NULL COMMENT 'Client IP address',
                    user_agent TEXT NULL COMMENT 'User agent string',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_endpoint (endpoint),
                    INDEX idx_method (method),
                    INDEX idx_status_code (status_code),
                    INDEX idx_created_at (created_at),
                    INDEX idx_endpoint_created (endpoint, created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            execute_update(create_app_metrics_table)
            print("Application metrics table ready")
        except Exception as e:
            print(f"Warning: Could not create application_metrics table: {str(e)}")
    else:
        print("Warning: Database connection test failed")
else:
    print("Warning: Database pool initialization failed")


# ============================================
# APPLICATION METRICS TRACKING MIDDLEWARE
# ============================================

@app.before_request
def track_request_start():
    """Track request start time for response time calculation"""
    request.start_time = time.time()

@app.after_request
def track_request_metrics(response):
    """Track application metrics for each API request"""
    try:
        # Skip tracking for static files and certain endpoints
        path = request.path
        if (path.startswith('/static/') or 
            path.startswith('/images/') or 
            path.startswith('/favicon') or
            path == '/' or
            'metrics' in path.lower()):  # Don't track metrics endpoints to avoid recursion
            return response
        
        # Calculate response time
        if hasattr(request, 'start_time'):
            response_time_ms = (time.time() - request.start_time) * 1000
        else:
            response_time_ms = 0
        
        # Get request details
        endpoint = path
        method = request.method
        status_code = response.status_code
        is_error = status_code >= 400
        ip_address = get_client_ip()
        user_agent = request.headers.get('User-Agent', '')[:500]  # Limit length
        
        # Store metrics in database (async in background to avoid slowing down requests)
        def store_metrics():
            try:
                query = """
                    INSERT INTO application_metrics 
                    (endpoint, method, response_time_ms, status_code, is_error, ip_address, user_agent)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                execute_update(query, (
                    endpoint, method, response_time_ms, status_code, 
                    is_error, ip_address, user_agent
                ))
            except Exception as e:
                # Silently fail - don't break the request if metrics fail
                pass
        
        # Store in background thread
        thread = threading.Thread(target=store_metrics)
        thread.daemon = True
        thread.start()
        
    except Exception:
        # Silently fail - don't break the request if metrics fail
        pass
    
    return response


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_pagination_params() -> PaginationParams:
    """Get pagination parameters from request"""
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10
    if limit > 100:
        limit = 100
    return PaginationParams(page=page, limit=limit)


def calculate_pages(total: int, limit: int) -> int:
    """Calculate total pages"""
    return (total + limit - 1) // limit if total > 0 else 0


def save_base64_image(base64_string: str, images_dir: Path) -> str:
    """Convert base64 image to file and save it. Returns the relative URL path."""
    if not base64_string.startswith('data:image/'):
        return base64_string
    
    try:
        header, data = base64_string.split(',', 1)
        format_part = header.split(';')[0]
        image_format = format_part.split('/')[-1]
        
        image_data = base64.b64decode(data)
        
        property_images_dir = images_dir / "images" / "properties"
        property_images_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{uuid.uuid4()}.{image_format}"
        file_path = property_images_dir / filename
        
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        return f"/images/properties/{filename}"
    except Exception as e:
        print(f"Error saving base64 image: {e}")
        return base64_string


def save_partner_logo(logo_url: Optional[str], images_dir: Path) -> Optional[str]:
    """Process partner logo - convert base64 to file if needed."""
    if not logo_url:
        return None
    
    if not logo_url.startswith('data:image/'):
        return logo_url
    
    try:
        header, data = logo_url.split(',', 1)
        format_part = header.split(';')[0]
        image_format = format_part.split('/')[-1]
        
        image_data = base64.b64decode(data)
        
        logos_dir = images_dir / "images" / "logos"
        logos_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{uuid.uuid4()}.{image_format}"
        file_path = logos_dir / filename
        
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        return f"/images/logos/{filename}"
    except Exception as e:
        print(f"Error saving partner logo: {e}")
        return logo_url


def process_image_urls(image_urls: List[str], images_dir: Path) -> List[str]:
    """Process a list of image URLs, converting base64 to files if needed."""
    processed_urls = []
    for url in image_urls:
        if url and url.startswith('data:image/'):
            processed_url = save_base64_image(url, images_dir)
            processed_urls.append(processed_url)
        else:
            processed_urls.append(url)
    return processed_urls


def normalize_image_url(url: Optional[str]) -> Optional[str]:
    """Normalize image URL for frontend compatibility"""
    if not url:
        return None
    # If it's already a full URL (http/https), return as is
    if url.startswith('http://') or url.startswith('https://'):
        return url
    # If it's already a data URL (base64), return as is
    if url.startswith('data:'):
        return url
    
    # Handle server paths that include /public_html/ or /home/ directories
    # Extract the relative path after /public_html/ or find the last /images/ occurrence
    if '/public_html/' in url:
        # Extract path after /public_html/
        parts = url.split('/public_html/', 1)
        if len(parts) > 1:
            url = '/' + parts[1].lstrip('/')
    elif '/images/' in url:
        # Find the last occurrence of /images/ to handle cases like /images/home/.../images/logos/...
        last_images_index = url.rfind('/images/')
        if last_images_index >= 0:
            url = url[last_images_index:]
    
    # If it already starts with /images/ or /frontend/, return as is
    if url.startswith('/images/') or url.startswith('/frontend/'):
        return url
    clean_url = url.lstrip('/')
    return f"/images/{clean_url}"


# ============================================
# HELPER FUNCTIONS FOR ERROR HANDLING
# ============================================

def abort_with_message(status_code: int, message: str):
    """Helper function to abort with a custom error message"""
    response = make_response(jsonify({"error": message, "success": False}), status_code)
    abort(response)


# ============================================
# AUTHENTICATION & AUTHORIZATION
# ============================================

from functools import wraps

def require_admin_auth(f):
    """
    Decorator to require admin authentication for protected routes.
    Verifies user exists in database and has admin role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get admin email from environment
        allowed_admin_email = os.getenv("ADMIN_EMAIL")
        if not allowed_admin_email:
            abort_with_message(500, "Server configuration error: ADMIN_EMAIL not set")
        
        # Check for admin email in Authorization header or X-Admin-Email header
        # This is a simple auth mechanism - in production, consider using JWT tokens
        auth_email = request.headers.get('X-Admin-Email') or request.headers.get('Authorization')
        
        # If Authorization header, extract email (format: "Email <email>")
        if auth_email and auth_email.startswith('Email '):
            auth_email = auth_email.replace('Email ', '')
        
        # Validate email is provided
        if not auth_email:
            abort_with_message(401, "Unauthorized: Admin authentication required")
        
        # Normalize email for comparison
        auth_email = auth_email.lower().strip()
        allowed_admin_email = allowed_admin_email.lower().strip()
        
        # Verify email matches admin email from environment
        if auth_email != allowed_admin_email:
            abort_with_message(401, "Unauthorized: Admin authentication required")
        
        # Verify user exists in database and has admin role
        try:
            # Test database connection
            connection_test = test_connection()
            if not connection_test.get("connected", False):
                abort_with_message(500, "Database connection failed. Please try again later.")
            
            # Query user from database to verify they exist and have admin role
            user_query = "SELECT id, email, role, is_active FROM users WHERE email = %s AND is_active = 1 AND role = 'admin' LIMIT 1"
            users = execute_query(user_query, (auth_email,))
            
            if not users or len(users) == 0:
                abort_with_message(401, "Unauthorized: Admin authentication required")
            
            user = users[0]
            
            # Double-check user has admin role and is active
            if user.get('role') != 'admin' or not user.get('is_active'):
                abort_with_message(403, "Access denied: Admin role required")
            
        except Exception as db_error:
            error_msg = str(db_error)
            print(f"Database error during admin auth verification: {error_msg}")
            traceback.print_exc()
            # Don't expose database errors to client, just return unauthorized
            abort_with_message(401, "Unauthorized: Admin authentication required")
        
        return f(*args, **kwargs)
    return decorated_function


# ============================================
# ROUTES - AUTHENTICATION
# ============================================

@app.route("/api/auth/login", methods=["POST"])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        try:
            login_data = LoginSchema(**data)
        except Exception as validation_error:
            # Handle Pydantic validation errors
            error_msg = str(validation_error)
            if "email" in error_msg.lower():
                abort_with_message(400, "Invalid email format")
            elif "password" in error_msg.lower():
                abort_with_message(400, "Password is required")
            else:
                abort_with_message(400, f"Invalid request data: {error_msg}")
        
        allowed_admin_email = os.getenv("ADMIN_EMAIL")
        if not allowed_admin_email:
            abort_with_message(500, "Server configuration error: ADMIN_EMAIL not set")
        
        if login_data.email.lower() != allowed_admin_email.lower():
            abort_with_message(401, "Invalid email or password")
        
        # Test database connection before querying
        connection_test = test_connection()
        if not connection_test.get("connected", False):
            error_msg = connection_test.get("error", "Unknown database connection error")
            print(f"Database connection test failed during login: {error_msg}")
            print(f"Connection details: {connection_test.get('details', {})}")
            suggestion = connection_test.get("suggestion", "Please check database configuration in cPanel.")
            abort_with_message(500, f"Database connection failed: {error_msg}. {suggestion}")
        
        # Query user from database - verify email, active status, and admin role
        try:
            user_query = "SELECT * FROM users WHERE email = %s AND is_active = 1 AND role = 'admin'"
            users = execute_query(user_query, (login_data.email,))
        except Exception as db_error:
            error_msg = str(db_error)
            print(f"Database query error during login: {error_msg}")
            traceback.print_exc()
            # Provide specific error messages for common database issues
            if "Access denied" in error_msg or "(1045" in error_msg:
                abort_with_message(500, "Database authentication failed. Please verify DB_USER and DB_PASSWORD in cPanel environment variables.")
            elif "Can't connect" in error_msg or "Connection refused" in error_msg:
                abort_with_message(500, "Cannot connect to database server. Please verify DB_HOST in cPanel environment variables.")
            elif "Unknown database" in error_msg:
                abort_with_message(500, "Database not found. Please verify DB_NAME in cPanel environment variables.")
            else:
                abort_with_message(500, f"Database error during login: {error_msg}")
        
        if not users or len(users) == 0:
            abort_with_message(401, "Invalid email or password")
        
        user = users[0]
        
        # Verify password hash matches
        if not user.get('password_hash'):
            abort_with_message(401, "Invalid email or password")
        
        if not verify_password(login_data.password, user['password_hash']):
            abort_with_message(401, "Invalid email or password")
        
        # Double-check user has admin role
        if user.get('role') != 'admin':
            abort_with_message(403, "Access denied: Admin role required")
        
        # Update last login timestamp
        try:
            update_query = "UPDATE users SET last_login = %s WHERE id = %s"
            execute_update(update_query, (datetime.now(), user['id']))
        except Exception as update_error:
            # Log error but don't fail login if update fails
            print(f"Warning: Failed to update last_login timestamp: {str(update_error)}")
            # Continue with login even if timestamp update fails
        
        response_data = LoginResponseSchema(
            success=True,
            message="Login successful",
            token=None,
            user={
                "id": user['id'],
                "email": user['email'],
                "full_name": user.get('full_name'),
                "role": user.get('role', 'admin')
            }
        )
        return jsonify(response_data.model_dump())
    except RuntimeError as e:
        # Database connection errors
        error_msg = str(e)
        if "Database engine not initialized" in error_msg or "Check environment variables" in error_msg:
            print(f"Database configuration error during login: {error_msg}")
            traceback.print_exc()
            abort_with_message(500, "Database not configured. Please check environment variables in cPanel.")
        else:
            print(f"Database runtime error during login: {error_msg}")
            traceback.print_exc()
            abort_with_message(500, f"Database error: {error_msg}")
    except Exception as e:
        error_msg = str(e)
        print(f"Login error: {error_msg}")
        traceback.print_exc()
        # Check for common database connection errors
        if "Access denied" in error_msg or "(1045" in error_msg:
            abort_with_message(500, "Database authentication failed. Please verify DB_USER and DB_PASSWORD in cPanel environment variables.")
        elif "Can't connect" in error_msg or "Connection refused" in error_msg:
            abort_with_message(500, "Cannot connect to database server. Please verify DB_HOST in cPanel environment variables.")
        elif "Unknown database" in error_msg:
            abort_with_message(500, "Database not found. Please verify DB_NAME in cPanel environment variables.")
        else:
            abort_with_message(500, f"An error occurred during login: {error_msg}")


# ============================================
# ROUTES - HEALTH CHECK
# ============================================

@app.route("/", methods=["GET"])
def root():
    """Serve the main index page"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return send_file(str(index_path))
    return jsonify({
        "message": "Tirumakudalu Properties API",
        "version": "1.0.0",
        "status": "running"
    })


@app.route("/index.html", methods=["GET"])
def index_page_html():
    """Serve the index page (with .html extension)"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return send_file(str(index_path))
    abort_with_message(404, "Page not found")


@app.route("/api", methods=["GET"])
def api_root():
    """API root endpoint"""
    return jsonify({
        "message": "Tirumakudalu Properties API",
        "version": "1.0.0",
        "status": "running"
    })


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    db_status = test_connection()
    return jsonify({
        "status": "healthy" if db_status.get("connected", False) else "unhealthy",
        "database": "connected" if db_status.get("connected", False) else "disconnected",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/db/test", methods=["GET"])
def test_db_connection():
    """Test database connection and return detailed diagnostics"""
    try:
        from database import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, MYSQL_PORT, ENV_FILE
        from pathlib import Path
        
        # Check which variables are set
        env_status = {
            "DB_USER": "✓ Set" if MYSQL_USER else "✗ Missing",
            "DB_PASSWORD": "✓ Set" if MYSQL_PASSWORD else "✗ Missing",
            "DB_HOST": MYSQL_HOST or "✗ Missing",
            "DB_NAME": "✓ Set" if MYSQL_DB else "✗ Missing",
            "DB_PORT": MYSQL_PORT
        }
        
        # Check if .env file exists
        env_file_exists = ENV_FILE.exists() if ENV_FILE else False
        
        db_status = test_connection()
        if db_status.get("connected", False):
            return jsonify({
                "success": True,
                "connected": True,
                "message": "Database connection successful",
                "details": db_status.get("details", {}),
                "environment_status": env_status,
                "env_file_exists": env_file_exists,
                "env_file_path": str(ENV_FILE) if ENV_FILE else None,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "connected": False,
                "error": db_status.get("error", "Unknown error"),
                "details": db_status.get("details", {}),
                "environment_status": env_status,
                "env_file_exists": env_file_exists,
                "env_file_path": str(ENV_FILE) if ENV_FILE else None,
                "suggestion": db_status.get("suggestion", "Check database configuration"),
                "help": "For local development: Create a .env file in the project root (see .env.example). For cPanel: Set environment variables in cPanel settings.",
                "timestamp": datetime.now().isoformat()
            }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "connected": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# ============================================
# ROUTES - PROPERTIES
# ============================================

@app.route("/api/properties", methods=["GET"])
def get_properties():
    """Get all properties with filtering and pagination"""
    try:
        pagination = get_pagination_params()
        offset = (pagination.page - 1) * pagination.limit
        
        # Get query parameters
        type_str = request.args.get('type')
        status_str = request.args.get('status')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        location = request.args.get('location')
        is_featured = request.args.get('is_featured', type=lambda x: x.lower() == 'true' if x else None)
        is_active = request.args.get('is_active', default='true', type=lambda x: x.lower() == 'true' if x else True)
        
        # Build WHERE clause
        is_active_int = 1 if is_active else 0
        conditions = ["is_active = %s"]
        params = [is_active_int]
        
        if type_str:
            try:
                prop_type = PropertyType(type_str)
                conditions.append("type = %s")
                params.append(prop_type.value)
            except ValueError:
                pass
        
        if status_str:
            try:
                prop_status = PropertyStatus(status_str)
                conditions.append("status = %s")
                params.append(prop_status.value)
            except ValueError:
                pass
        
        if min_price is not None:
            conditions.append("price >= %s")
            params.append(min_price)
        
        if max_price is not None:
            conditions.append("price <= %s")
            params.append(max_price)
        
        if location:
            # Search in both city and locality fields
            conditions.append("(LOWER(city) LIKE %s OR LOWER(locality) LIKE %s)")
            params.append(f"%{location.lower()}%")
            params.append(f"%{location.lower()}%")
        
        if is_featured is not None:
            is_featured_int = 1 if is_featured else 0
            conditions.append("is_featured = %s")
            params.append(is_featured_int)
        
        where_clause = " AND ".join(conditions)
        
        # Build separate conditions for residential and plot properties
        # For plots, exclude type filter since they don't have a type field
        type_filter_index = None
        if type_str and "type = %s" in where_clause:
            # Find the index of type filter in conditions
            for i, cond in enumerate(conditions):
                if cond == "type = %s":
                    type_filter_index = i
                    break
        
        # Build params for residential (include type filter) and plot (exclude type filter)
        residential_params = list(params)
        plot_params = [p for i, p in enumerate(params) if i != type_filter_index] if type_filter_index is not None else list(params)
        
        # Build where clauses
        residential_where = where_clause
        plot_where = " AND ".join([c for i, c in enumerate(conditions) if i != type_filter_index]) if type_filter_index is not None else where_clause
        
        # Get total count from both tables
        count_res = execute_query(f"SELECT COUNT(*) as total FROM residential_properties WHERE {residential_where}", tuple(residential_params)) if residential_where else [{'total': 0}]
        count_plot = execute_query(f"SELECT COUNT(*) as total FROM plot_properties WHERE {plot_where}", tuple(plot_params)) if plot_where else [{'total': 0}]
        total = (count_res[0]['total'] if count_res else 0) + (count_plot[0]['total'] if count_plot else 0)
        
        # Query both tables separately and combine results
        import time
        query_start = time.time()
        
        # Query residential properties
        residential_query = f"""
            SELECT 
                id, city, locality, property_name as title, property_name, 
                unit_type, bedrooms, buildup_area as area, buildup_area, carpet_area, 
                price, price_text, price_negotiable, price_includes_registration,
                type, status, property_status, description,
                is_featured, is_active, created_at, updated_at,
                'residential' as property_category,
                NULL as plot_area, NULL as plot_length, NULL as plot_breadth,
                NULL as project_name, 0 as bathrooms
            FROM residential_properties
            WHERE {residential_where}
            ORDER BY created_at DESC
        """
        residential_props = execute_query(residential_query, tuple(residential_params)) if residential_where else []
        
        # Query plot properties (only if no type filter is set, since plots don't have a type field)
        plot_props = []
        if type_filter_index is None:
            plot_query = f"""
                SELECT 
                    id, city, locality, project_name as title, project_name as property_name,
                    NULL as unit_type, 0 as bedrooms, plot_area as area, NULL as buildup_area, NULL as carpet_area,
                    price, price_text, price_negotiable, price_includes_registration,
                    'plot' as type, status, property_status, description,
                    is_featured, is_active, created_at, updated_at,
                    'plot' as property_category,
                    plot_area, plot_length, plot_breadth,
                    project_name, 0 as bathrooms
                FROM plot_properties
                WHERE {plot_where}
                ORDER BY created_at DESC
            """
            plot_props = execute_query(plot_query, tuple(plot_params)) if plot_where else []
        
        # Combine and sort by created_at
        all_properties = residential_props + plot_props
        all_properties.sort(key=lambda x: x.get('created_at', datetime.min), reverse=True)
        
        # Apply pagination
        properties = all_properties[offset:offset + pagination.limit]
        
        query_time = time.time() - query_start
        
        if query_time > 1.0:  # Log slow queries (> 1 second)
            print(f"[PERF] Slow query detected: {query_time:.2f}s for page {pagination.page}, limit {pagination.limit}")
        
        # Fetch primary images for each property and normalize image URLs
        normalized_properties = []
        for prop in properties:
            prop_dict = dict(prop)
            property_id = prop_dict.get('id')
            property_category = prop_dict.get('property_category', 'residential')
            
            # Fetch primary image from the new image tables (project, floorplan, masterplan)
            if property_id:
                try:
                    if property_category == 'residential':
                        primary_image_query = """
                            SELECT image_url 
                            FROM (
                                SELECT image_url, image_order, created_at
                                FROM residential_property_project_images
                                WHERE property_id = %s
                                UNION ALL
                                SELECT image_url, image_order, created_at
                                FROM residential_property_floorplan_images
                                WHERE property_id = %s
                                UNION ALL
                                SELECT image_url, image_order, created_at
                                FROM residential_property_masterplan_images
                                WHERE property_id = %s
                            ) AS all_images
                            ORDER BY image_order ASC, created_at ASC 
                            LIMIT 1
                        """
                        all_images_query = """
                            SELECT image_url 
                            FROM (
                                SELECT image_url, image_order, created_at
                                FROM residential_property_project_images
                                WHERE property_id = %s
                                UNION ALL
                                SELECT image_url, image_order, created_at
                                FROM residential_property_floorplan_images
                                WHERE property_id = %s
                                UNION ALL
                                SELECT image_url, image_order, created_at
                                FROM residential_property_masterplan_images
                                WHERE property_id = %s
                            ) AS all_images
                            ORDER BY image_order ASC, created_at ASC
                        """
                    else:
                        primary_image_query = """
                            SELECT image_url 
                            FROM (
                                SELECT image_url, image_order, created_at
                                FROM plot_property_project_images
                                WHERE property_id = %s
                                UNION ALL
                                SELECT image_url, image_order, created_at
                                FROM plot_property_floorplan_images
                                WHERE property_id = %s
                                UNION ALL
                                SELECT image_url, image_order, created_at
                                FROM plot_property_masterplan_images
                                WHERE property_id = %s
                            ) AS all_images
                            ORDER BY image_order ASC, created_at ASC 
                            LIMIT 1
                        """
                        all_images_query = """
                            SELECT image_url 
                            FROM (
                                SELECT image_url, image_order, created_at
                                FROM plot_property_project_images
                                WHERE property_id = %s
                                UNION ALL
                                SELECT image_url, image_order, created_at
                                FROM plot_property_floorplan_images
                                WHERE property_id = %s
                                UNION ALL
                                SELECT image_url, image_order, created_at
                                FROM plot_property_masterplan_images
                                WHERE property_id = %s
                            ) AS all_images
                            ORDER BY image_order ASC, created_at ASC
                        """
                    
                    primary_images = execute_query(primary_image_query, (property_id, property_id, property_id))
                    if primary_images and primary_images[0].get('image_url'):
                        prop_dict['primary_image'] = normalize_image_url(primary_images[0]['image_url'])
                    
                    # Also fetch all images for the property
                    all_images = execute_query(all_images_query, (property_id, property_id, property_id))
                    if all_images:
                        prop_dict['images'] = [
                            {'image_url': normalize_image_url(img['image_url'])} 
                            for img in all_images 
                            if img.get('image_url')
                        ]
                except Exception as e:
                    # If image fetch fails, continue without images
                    print(f"Warning: Could not fetch images for property {property_id}: {str(e)}")
                    prop_dict['images'] = []
            
            # Normalize existing primary_image if it exists (fallback - in case property table has primary_image field)
            if 'primary_image' in prop_dict and prop_dict['primary_image']:
                prop_dict['primary_image'] = normalize_image_url(prop_dict['primary_image'])
            
            # Ensure images array exists
            if 'images' not in prop_dict:
                prop_dict['images'] = []
            
            normalized_properties.append(prop_dict)
        
        response = PaginatedResponse(
            total=total,
            page=pagination.page,
            limit=pagination.limit,
            pages=calculate_pages(total, pagination.limit),
            items=normalized_properties
        )
        return jsonify(response.dict())
    except RuntimeError as e:
        # Database connection errors
        error_msg = str(e)
        if "Database engine not initialized" in error_msg or "Check environment variables" in error_msg:
            print(f"Database configuration error: {error_msg}")
            traceback.print_exc()
            # Provide more helpful error message
            from database import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, ENV_FILE
            missing = []
            if not MYSQL_USER:
                missing.append("DB_USER")
            if not MYSQL_PASSWORD:
                missing.append("DB_PASSWORD")
            if not MYSQL_DB:
                missing.append("DB_NAME")
            
            error_detail = f"Missing environment variables: {', '.join(missing)}. "
            if ENV_FILE.exists():
                error_detail += f"Check your .env file at {ENV_FILE}"
            else:
                error_detail += f"For local development, create a .env file (see .env.example). For cPanel, set variables in cPanel settings."
            abort_with_message(500, error_detail)
        else:
            print(f"Database runtime error: {error_msg}")
            traceback.print_exc()
            abort_with_message(500, f"Database error: {error_msg}")
    except Exception as e:
        error_msg = str(e)
        print(f"Error fetching properties: {error_msg}")
        traceback.print_exc()
        # Check for common database connection errors
        if "Access denied" in error_msg or "(1045" in error_msg:
            abort_with_message(500, "Database authentication failed. Please verify DB_USER and DB_PASSWORD in cPanel environment variables.")
        elif "Can't connect" in error_msg or "Connection refused" in error_msg:
            abort_with_message(500, "Cannot connect to database server. Please verify DB_HOST in cPanel environment variables.")
        elif "Unknown database" in error_msg:
            abort_with_message(500, "Database not found. Please verify DB_NAME in cPanel environment variables.")
        else:
            abort_with_message(500, f"Error fetching properties: {error_msg}")


@app.route("/api/properties/<int:property_id>", methods=["GET"])
def get_property(property_id: int):
    """Get a single property by ID with images and features"""
    try:
        # Check residential_properties first
        residential_query = """
            SELECT 
                id, city, locality, property_name as title, property_name, 
                unit_type, bedrooms, buildup_area as area, buildup_area, carpet_area, 
                price, price_text, price_negotiable, price_includes_registration,
                type, status, property_status, description,
                is_featured, is_active, created_at, updated_at,
                'residential' as property_category,
                NULL as plot_area, NULL as plot_length, NULL as plot_breadth,
                NULL as project_name, 0 as bathrooms
            FROM residential_properties
            WHERE id = %s
        """
        properties = execute_query(residential_query, (property_id,))
        property_category = 'residential'
        feature_table = 'residential_property_features'
        
        # If not found in residential, check plot_properties
        if not properties:
            plot_query = """
                SELECT 
                    id, city, locality, project_name as title, project_name as property_name,
                    NULL as unit_type, 0 as bedrooms, plot_area as area, NULL as buildup_area, NULL as carpet_area,
                    price, price_text, price_negotiable, price_includes_registration,
                    'plot' as type, status, property_status, description,
                    is_featured, is_active, created_at, updated_at,
                    'plot' as property_category,
                    plot_area, plot_length, plot_breadth,
                    project_name, 0 as bathrooms
                FROM plot_properties
                WHERE id = %s
            """
            properties = execute_query(plot_query, (property_id,))
            property_category = 'plot'
            feature_table = 'plot_property_features'
        
        if not properties:
            abort_with_message(404, "Property not found")
        
        property_data = dict(properties[0])
        
        # Construct location from city and locality if not already present
        if 'location' not in property_data or not property_data.get('location'):
            city = property_data.get('city', '')
            locality = property_data.get('locality', '')
            if city and locality:
                property_data['location'] = f"{city}, {locality}"
            elif city:
                property_data['location'] = city
            elif locality:
                property_data['location'] = locality
            else:
                property_data['location'] = 'Location not specified'
        
        # Get images from the new image tables (project, floorplan, masterplan)
        if property_category == 'residential':
            images_query = """
                SELECT id, property_id, image_url, image_order, created_at, 'project' as image_type
                FROM residential_property_project_images
                WHERE property_id = %s
                UNION ALL
                SELECT id, property_id, image_url, image_order, created_at, 'floorplan' as image_type
                FROM residential_property_floorplan_images
                WHERE property_id = %s
                UNION ALL
                SELECT id, property_id, image_url, image_order, created_at, 'masterplan' as image_type
                FROM residential_property_masterplan_images
                WHERE property_id = %s
                ORDER BY image_order, created_at
            """
            images = execute_query(images_query, (property_id, property_id, property_id))
        else:
            images_query = """
                SELECT id, property_id, image_url, image_order, created_at, 'project' as image_type
                FROM plot_property_project_images
                WHERE property_id = %s
                UNION ALL
                SELECT id, property_id, image_url, image_order, created_at, 'floorplan' as image_type
                FROM plot_property_floorplan_images
                WHERE property_id = %s
                UNION ALL
                SELECT id, property_id, image_url, image_order, created_at, 'masterplan' as image_type
                FROM plot_property_masterplan_images
                WHERE property_id = %s
                ORDER BY image_order, created_at
            """
            images = execute_query(images_query, (property_id, property_id, property_id))
        
        # Separate images by type and normalize URLs
        project_images = []
        floorplan_images = []
        masterplan_images = []
        
        for img in images:
            img_dict = dict(img)
            if 'image_url' in img_dict and img_dict['image_url']:
                img_dict['image_url'] = normalize_image_url(img_dict['image_url'])
            
            # Remove image_type from dict as it's not part of the schema
            image_type = img_dict.pop('image_type', None)
            
            # Categorize images by type
            if image_type == 'project':
                project_images.append(img_dict)
            elif image_type == 'floorplan':
                floorplan_images.append(img_dict)
            elif image_type == 'masterplan':
                masterplan_images.append(img_dict)
        
        # Assign to correct fields in property_data
        property_data['images'] = []  # Empty list - PropertyImageSchema requires is_primary which these images don't have
        property_data['project_images'] = project_images
        property_data['floorplan_images'] = floorplan_images
        property_data['masterplan_images'] = masterplan_images
        
        # Get features from the appropriate table
        features_query = f"SELECT * FROM {feature_table} WHERE property_id = %s ORDER BY feature_name"
        features = execute_query(features_query, (property_id,))
        property_data['features'] = [dict(feat) for feat in features]
        
        response = PropertyResponseSchema(**property_data)
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error fetching property: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching property: {str(e)}")


@app.route("/api/properties", methods=["POST"])
@require_admin_auth
def create_property():
    """Create a new property (deprecated - use /api/residential-properties or /api/plot-properties)"""
    abort_with_message(400, "Please use /api/residential-properties or /api/plot-properties endpoints")


@app.route("/api/residential-properties", methods=["POST"])
@require_admin_auth
def create_residential_property():
    """Create a new residential property"""
    try:
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        # Extract required fields
        city = data.get('city')
        locality = data.get('locality')
        property_name = data.get('property_name')
        unit_type = data.get('unit_type', 'bhk')
        bedrooms = int(data.get('bedrooms', 1))
        buildup_area = float(data.get('buildup_area', 0))
        carpet_area = float(data.get('carpet_area', 0))
        price = float(data.get('price', 0))
        price_text = data.get('price_text')
        price_negotiable = 1 if data.get('price_negotiable') else 0
        price_includes_registration = 1 if data.get('price_includes_registration') else 0
        property_type = data.get('type', 'apartment')
        status = data.get('status', 'sale')
        # Validate status matches database CHECK constraint: ('sale', 'rent', 'resale', 'new')
        if status not in ['sale', 'rent', 'resale', 'new']:
            abort_with_message(400, f"Invalid status value: {status}. Must be one of: sale, rent, resale, new")
        property_status = data.get('property_status')
        description = data.get('description')
        is_featured = 1 if data.get('is_featured') else 0
        is_active = 1 if data.get('is_active', True) else 0
        images = data.get('images', [])
        features = data.get('features', []) or data.get('amenities', [])
        
        if not city or not locality or not property_name:
            abort_with_message(400, "City, locality, and property_name are required")
        
        insert_query = """
            INSERT INTO residential_properties (
                city, locality, property_name, unit_type, bedrooms, buildup_area, carpet_area,
                price, price_text, price_negotiable, price_includes_registration,
                type, status, property_status, description,
                is_featured, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        with get_db_cursor() as cursor:
            cursor.execute(insert_query, (
                city, locality, property_name, unit_type, bedrooms, buildup_area, carpet_area,
                price, price_text, price_negotiable, price_includes_registration,
                property_type, status, property_status, description,
                is_featured, is_active
            ))
            property_id = cursor.lastrowid
            
            # Insert images into project_images table (default category)
            if images:
                processed_images = process_image_urls(images, FRONTEND_DIR)
                for idx, image_url in enumerate(processed_images):
                    image_query = "INSERT INTO residential_property_project_images (property_id, image_url, image_order) VALUES (%s, %s, %s)"
                    cursor.execute(image_query, (property_id, image_url, idx))
            
            # Insert features
            if features:
                for feature_name in features:
                    feature_query = "INSERT IGNORE INTO residential_property_features (property_id, feature_name) VALUES (%s, %s)"
                    cursor.execute(feature_query, (property_id, feature_name))
        
        return jsonify({"message": "Residential property created successfully", "id": property_id}), 201
    except Exception as e:
        print(f"Error creating residential property: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error creating residential property: {str(e)}")


@app.route("/api/plot-properties", methods=["POST"])
@require_admin_auth
def create_plot_property():
    """Create a new plot property"""
    try:
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        # Extract required fields
        city = data.get('city')
        locality = data.get('locality')
        project_name = data.get('project_name')
        plot_area = float(data.get('plot_area', 0))
        plot_length = float(data.get('plot_length', 0))
        plot_breadth = float(data.get('plot_breadth', 0))
        price = float(data.get('price', 0))
        price_text = data.get('price_text')
        price_negotiable = 1 if data.get('price_negotiable') else 0
        price_includes_registration = 1 if data.get('price_includes_registration') else 0
        status = data.get('status', 'sale')
        # Validate status matches database CHECK constraint: ('sale', 'rent', 'resale', 'new')
        if status not in ['sale', 'rent', 'resale', 'new']:
            abort_with_message(400, f"Invalid status value: {status}. Must be one of: sale, rent, resale, new")
        property_status = data.get('property_status')
        description = data.get('description')
        is_featured = 1 if data.get('is_featured') else 0
        is_active = 1 if data.get('is_active', True) else 0
        images = data.get('images', [])
        features = data.get('features', []) or data.get('amenities', [])
        
        if not city or not locality or not project_name:
            abort_with_message(400, "City, locality, and project_name are required")
        
        insert_query = """
            INSERT INTO plot_properties (
                city, locality, project_name, plot_area, plot_length, plot_breadth,
                price, price_text, price_negotiable, price_includes_registration,
                status, property_status, description,
                is_featured, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        with get_db_cursor() as cursor:
            cursor.execute(insert_query, (
                city, locality, project_name, plot_area, plot_length, plot_breadth,
                price, price_text, price_negotiable, price_includes_registration,
                status, property_status, description,
                is_featured, is_active
            ))
            property_id = cursor.lastrowid
            
            # Insert images into project_images table (default category)
            if images:
                processed_images = process_image_urls(images, FRONTEND_DIR)
                for idx, image_url in enumerate(processed_images):
                    image_query = "INSERT INTO plot_property_project_images (property_id, image_url, image_order) VALUES (%s, %s, %s)"
                    cursor.execute(image_query, (property_id, image_url, idx))
            
            # Insert features
            if features:
                for feature_name in features:
                    feature_query = "INSERT IGNORE INTO plot_property_features (property_id, feature_name) VALUES (%s, %s)"
                    cursor.execute(feature_query, (property_id, feature_name))
        
        return jsonify({"message": "Plot property created successfully", "id": property_id}), 201
    except Exception as e:
        print(f"Error creating plot property: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error creating plot property: {str(e)}")


@app.route("/api/properties/<int:property_id>", methods=["PUT"])
@require_admin_auth
def update_property(property_id: int):
    """Update a property"""
    try:
        existing = execute_query("SELECT id FROM properties WHERE id = %s", (property_id,))
        if not existing:
            abort_with_message(404, "Property not found")
        
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        property_data = PropertyUpdateSchema(**data)
        
        # Build update query
        updates = []
        params = []
        
        if property_data.title is not None:
            updates.append("title = %s")
            params.append(property_data.title)
        if property_data.location is not None:
            updates.append("location = %s")
            params.append(property_data.location)
        if property_data.price is not None:
            updates.append("price = %s")
            params.append(property_data.price)
        if property_data.price_text is not None:
            updates.append("price_text = %s")
            params.append(property_data.price_text)
        if property_data.type is not None:
            updates.append("type = %s")
            params.append(property_data.type.value)
        if property_data.bedrooms is not None:
            updates.append("bedrooms = %s")
            params.append(property_data.bedrooms)
        if property_data.bathrooms is not None:
            updates.append("bathrooms = %s")
            params.append(property_data.bathrooms)
        if property_data.area is not None:
            updates.append("area = %s")
            params.append(property_data.area)
        if property_data.status is not None:
            updates.append("status = %s")
            params.append(property_data.status.value)
        if property_data.description is not None:
            updates.append("description = %s")
            params.append(property_data.description)
        if property_data.is_featured is not None:
            updates.append("is_featured = %s")
            params.append(property_data.is_featured)
        if property_data.is_active is not None:
            updates.append("is_active = %s")
            params.append(property_data.is_active)
        
        if updates:
            params.append(property_id)
            update_query = f"UPDATE properties SET {', '.join(updates)} WHERE id = %s"
            execute_update(update_query, tuple(params))
        
        # Update images if provided
        if property_data.images is not None:
            processed_images = process_image_urls(property_data.images, FRONTEND_DIR)
            with get_db_cursor() as cursor:
                cursor.execute("DELETE FROM property_images WHERE property_id = %s", (property_id,))
                for idx, image_url in enumerate(processed_images):
                    cursor.execute(
                        "INSERT INTO property_images (property_id, image_url, image_order, is_primary) VALUES (%s, %s, %s, %s)",
                        (property_id, image_url, idx, 1 if idx == 0 else 0)
                    )
        
        # Update features if provided
        if property_data.features is not None:
            with get_db_cursor() as cursor:
                cursor.execute("DELETE FROM property_features WHERE property_id = %s", (property_id,))
                for feature_name in property_data.features:
                    cursor.execute(
                        "INSERT IGNORE INTO property_features (property_id, feature_name) VALUES (%s, %s)",
                        (property_id, feature_name)
                    )
        
        # Return updated property
        property_query = "SELECT * FROM properties WHERE id = %s"
        properties = execute_query(property_query, (property_id,))
        property_data_dict = dict(properties[0])
        
        images_query = "SELECT * FROM property_images WHERE property_id = %s ORDER BY image_order, created_at"
        images = execute_query(images_query, (property_id,))
        normalized_images = []
        for img in images:
            img_dict = dict(img)
            if 'image_url' in img_dict and img_dict['image_url']:
                img_dict['image_url'] = normalize_image_url(img_dict['image_url'])
            normalized_images.append(img_dict)
        property_data_dict['images'] = normalized_images
        
        features_query = "SELECT * FROM property_features WHERE property_id = %s ORDER BY feature_name"
        features = execute_query(features_query, (property_id,))
        property_data_dict['features'] = [dict(feat) for feat in features]
        
        response = PropertyResponseSchema(**property_data_dict)
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error updating property: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error updating property: {str(e)}")


@app.route("/api/properties/<int:property_id>", methods=["DELETE"])
@require_admin_auth
def delete_property(property_id: int):
    """Delete a property"""
    try:
        # Check which table contains the property (residential or plot)
        # First check residential_properties
        residential_check = execute_query(
            "SELECT id FROM residential_properties WHERE id = %s",
            (property_id,)
        )
        
        if residential_check:
            # Delete from residential_properties (CASCADE will handle images and features)
            result = execute_update(
                "DELETE FROM residential_properties WHERE id = %s",
                (property_id,)
            )
        else:
            # Check plot_properties
            plot_check = execute_query(
                "SELECT id FROM plot_properties WHERE id = %s",
                (property_id,)
            )
            
            if plot_check:
                # Delete from plot_properties (CASCADE will handle images and features)
                result = execute_update(
                    "DELETE FROM plot_properties WHERE id = %s",
                    (property_id,)
                )
            else:
                abort_with_message(404, "Property not found")
        
        if result == 0:
            abort_with_message(404, "Property not found")
        
        response = MessageResponse(message="Property deleted successfully")
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error deleting property: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error deleting property: {str(e)}")


# ============================================
# ROUTES - PARTNERS
# ============================================

@app.route("/api/partners", methods=["GET"])
def get_partners():
    """Get all partners"""
    try:
        is_active_str = request.args.get('is_active', '').lower()
        is_active = None
        if is_active_str == 'true':
            is_active = True
        elif is_active_str == 'false':
            is_active = False
        
        if is_active is not None:
            is_active_int = 1 if is_active else 0
            query = "SELECT * FROM partners WHERE is_active = %s ORDER BY display_order, name"
            partners = execute_query(query, (is_active_int,))
        else:
            query = "SELECT * FROM partners ORDER BY display_order, name"
            partners = execute_query(query)
        
        normalized_partners = []
        for p in partners:
            try:
                partner_dict = dict(p)
                # Ensure all required fields are present
                if 'is_active' not in partner_dict:
                    partner_dict['is_active'] = True
                elif isinstance(partner_dict['is_active'], int):
                    partner_dict['is_active'] = bool(partner_dict['is_active'])
                if 'display_order' not in partner_dict:
                    partner_dict['display_order'] = 0
                if 'description' not in partner_dict:
                    partner_dict['description'] = None
                if 'created_at' not in partner_dict:
                    partner_dict['created_at'] = None
                if 'updated_at' not in partner_dict:
                    partner_dict['updated_at'] = None
                
                if 'logo_url' in partner_dict and partner_dict['logo_url']:
                    partner_dict['logo_url'] = normalize_image_url(partner_dict['logo_url'])
                
                normalized_partners.append(PartnerResponseSchema(**partner_dict))
            except Exception as schema_error:
                print(f"Error converting partner {p.get('id', 'unknown')}: {str(schema_error)}")
                traceback.print_exc()
                continue
        
        result = [p.dict() for p in normalized_partners]
        print(f"Successfully fetched {len(result)} partners (is_active filter: {is_active})")
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching partners: {str(e)}")
        traceback.print_exc()
        return jsonify([])


@app.route("/api/partners/<int:partner_id>", methods=["GET"])
def get_partner(partner_id: int):
    """Get a single partner by ID"""
    try:
        partners = execute_query("SELECT * FROM partners WHERE id = %s", (partner_id,))
        if not partners:
            abort_with_message(404, "Partner not found")
        
        partner_dict = dict(partners[0])
        if 'logo_url' in partner_dict:
            partner_dict['logo_url'] = normalize_image_url(partner_dict['logo_url'])
        
        response = PartnerResponseSchema(**partner_dict)
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error fetching partner: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching partner: {str(e)}")


@app.route("/api/partners", methods=["POST"])
@require_admin_auth
def create_partner():
    """Create a new partner"""
    try:
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        partner_data = PartnerCreateSchema(**data)
        processed_logo_url = save_partner_logo(partner_data.logo_url, FRONTEND_DIR)
        
        query = "INSERT INTO partners (name, logo_url, website_url, is_active, display_order) VALUES (%s, %s, %s, %s, %s)"
        with get_db_cursor() as cursor:
            cursor.execute(query, (
                partner_data.name, processed_logo_url, str(partner_data.website_url) if partner_data.website_url else None,
                partner_data.is_active, partner_data.display_order
            ))
            partner_id = cursor.lastrowid
        
        partners = execute_query("SELECT * FROM partners WHERE id = %s", (partner_id,))
        partner_dict = dict(partners[0])
        if 'logo_url' in partner_dict:
            partner_dict['logo_url'] = normalize_image_url(partner_dict['logo_url'])
        
        response = PartnerResponseSchema(**partner_dict)
        return jsonify(response.dict()), 201
    except Exception as e:
        print(f"Error creating partner: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error creating partner: {str(e)}")


@app.route("/api/partners/<int:partner_id>", methods=["PUT"])
@require_admin_auth
def update_partner(partner_id: int):
    """Update a partner"""
    try:
        existing = execute_query("SELECT id FROM partners WHERE id = %s", (partner_id,))
        if not existing:
            abort_with_message(404, "Partner not found")
        
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        try:
            partner_data = PartnerUpdateSchema(**data)
        except ValidationError as e:
            error_messages = []
            for error in e.errors():
                field = '.'.join(str(loc) for loc in error['loc'])
                message = error['msg']
                error_messages.append(f"{field}: {message}")
            abort_with_message(400, f"Validation error: {', '.join(error_messages)}")
        
        updates = []
        params = []
        
        if partner_data.name is not None:
            updates.append("name = %s")
            params.append(partner_data.name)
        if partner_data.logo_url is not None:
            processed_logo_url = save_partner_logo(partner_data.logo_url, FRONTEND_DIR)
            updates.append("logo_url = %s")
            params.append(processed_logo_url)
        if partner_data.website_url is not None:
            updates.append("website_url = %s")
            params.append(partner_data.website_url)
        if partner_data.is_active is not None:
            updates.append("is_active = %s")
            params.append(partner_data.is_active)
        if partner_data.display_order is not None:
            updates.append("display_order = %s")
            params.append(partner_data.display_order)
        
        if updates:
            params.append(partner_id)
            update_query = f"UPDATE partners SET {', '.join(updates)} WHERE id = %s"
            execute_update(update_query, tuple(params))
        
        partners = execute_query("SELECT * FROM partners WHERE id = %s", (partner_id,))
        partner_dict = dict(partners[0])
        if 'logo_url' in partner_dict:
            partner_dict['logo_url'] = normalize_image_url(partner_dict['logo_url'])
        
        response = PartnerResponseSchema(**partner_dict)
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error updating partner: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error updating partner: {str(e)}")


@app.route("/api/partners/<int:partner_id>", methods=["DELETE"])
@require_admin_auth
def delete_partner(partner_id: int):
    """Delete a partner"""
    try:
        result = execute_update("DELETE FROM partners WHERE id = %s", (partner_id,))
        if result == 0:
            abort_with_message(404, "Partner not found")
        response = MessageResponse(message="Partner deleted successfully")
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error deleting partner: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error deleting partner: {str(e)}")


# ============================================
# ROUTES - TESTIMONIALS
# ============================================

@app.route("/api/testimonials", methods=["GET"])
def get_testimonials():
    """Get all testimonials (public endpoint - only approved)"""
    try:
        is_approved = request.args.get('is_approved', default='true', type=lambda x: x.lower() == 'true' if x else True)
        is_featured = request.args.get('is_featured', type=lambda x: x.lower() == 'true' if x else None)
        
        is_approved_int = 1 if is_approved else 0
        conditions = ["is_approved = %s"]
        params = [is_approved_int]
        
        if is_featured is not None:
            is_featured_int = 1 if is_featured else 0
            conditions.append("is_featured = %s")
            params.append(is_featured_int)
        
        where_clause = " AND ".join(conditions)
        query = f"SELECT * FROM testimonials WHERE {where_clause} ORDER BY created_at DESC"
        
        testimonials = execute_query(query, tuple(params))
        
        result = []
        for t in testimonials:
            try:
                testimonial_dict = dict(t)
                if 'is_featured' not in testimonial_dict:
                    testimonial_dict['is_featured'] = False
                if 'created_at' not in testimonial_dict:
                    testimonial_dict['created_at'] = None
                result.append(TestimonialPublicSchema(**testimonial_dict))
            except Exception as schema_error:
                print(f"Error converting testimonial {t.get('id', 'unknown')}: {str(schema_error)}")
                continue
        
        return jsonify([r.dict() for r in result])
    except Exception as e:
        print(f"Error fetching testimonials: {str(e)}")
        traceback.print_exc()
        return jsonify([])


@app.route("/api/admin/testimonials", methods=["GET"])
@require_admin_auth
def get_all_testimonials():
    """Get all testimonials (admin endpoint)"""
    try:
        testimonials = execute_query("SELECT * FROM testimonials ORDER BY created_at DESC")
        result = [TestimonialResponseSchema(**dict(t)) for t in testimonials]
        return jsonify([r.dict() for r in result])
    except Exception as e:
        print(f"Error fetching testimonials: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching testimonials: {str(e)}")


@app.route("/api/testimonials", methods=["POST"])
def create_testimonial():
    """Create a new testimonial"""
    try:
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        testimonial_data = TestimonialCreateSchema(**data)
        
        query = """
            INSERT INTO testimonials (
                client_name, client_email, client_phone, service_type,
                rating, message, is_approved, is_featured
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (
                testimonial_data.client_name, testimonial_data.client_email,
                testimonial_data.client_phone, testimonial_data.service_type,
                testimonial_data.rating, testimonial_data.message,
                testimonial_data.is_approved, testimonial_data.is_featured
            ))
            testimonial_id = cursor.lastrowid
        
        # Send self-notification email in background
        def send_notification():
            send_self_notification_email(
                "new_testimonial",
                "New Testimonial Submitted",
                f"A new testimonial has been submitted by {testimonial_data.client_name}. Please review and approve it in your dashboard.",
                {
                    "Client Name": testimonial_data.client_name,
                    "Client Email": testimonial_data.client_email,
                    "Client Phone": testimonial_data.client_phone or "Not provided",
                    "Service Type": testimonial_data.service_type,
                    "Rating": f"{testimonial_data.rating}/5",
                    "Is Approved": "Yes" if testimonial_data.is_approved else "No (Needs Review)",
                    "Testimonial ID": testimonial_id
                }
            )
        
        thread = threading.Thread(target=send_notification)
        thread.daemon = True
        thread.start()
        
        result = execute_query("SELECT * FROM testimonials WHERE id = %s", (testimonial_id,))
        response = TestimonialResponseSchema(**dict(result[0]))
        return jsonify(response.dict()), 201
    except Exception as e:
        print(f"Error creating testimonial: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error creating testimonial: {str(e)}")


@app.route("/api/testimonials/<int:testimonial_id>", methods=["PUT"])
@require_admin_auth
def update_testimonial(testimonial_id: int):
    """Update a testimonial"""
    try:
        existing = execute_query("SELECT id FROM testimonials WHERE id = %s", (testimonial_id,))
        if not existing:
            abort_with_message(404, "Testimonial not found")
        
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        testimonial_data = TestimonialUpdateSchema(**data)
        
        updates = []
        params = []
        
        if testimonial_data.client_name is not None:
            updates.append("client_name = %s")
            params.append(testimonial_data.client_name)
        if testimonial_data.client_email is not None:
            updates.append("client_email = %s")
            params.append(testimonial_data.client_email)
        if testimonial_data.client_phone is not None:
            updates.append("client_phone = %s")
            params.append(testimonial_data.client_phone)
        if testimonial_data.service_type is not None:
            updates.append("service_type = %s")
            params.append(testimonial_data.service_type)
        if testimonial_data.rating is not None:
            updates.append("rating = %s")
            params.append(testimonial_data.rating)
        if testimonial_data.message is not None:
            updates.append("message = %s")
            params.append(testimonial_data.message)
        if testimonial_data.is_approved is not None:
            updates.append("is_approved = %s")
            params.append(testimonial_data.is_approved)
        if testimonial_data.is_featured is not None:
            updates.append("is_featured = %s")
            params.append(testimonial_data.is_featured)
        
        if updates:
            params.append(testimonial_id)
            update_query = f"UPDATE testimonials SET {', '.join(updates)} WHERE id = %s"
            execute_update(update_query, tuple(params))
        
        result = execute_query("SELECT * FROM testimonials WHERE id = %s", (testimonial_id,))
        response = TestimonialResponseSchema(**dict(result[0]))
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error updating testimonial: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error updating testimonial: {str(e)}")


@app.route("/api/testimonials/<int:testimonial_id>", methods=["DELETE"])
@require_admin_auth
def delete_testimonial(testimonial_id: int):
    """Delete a testimonial"""
    try:
        result = execute_update("DELETE FROM testimonials WHERE id = %s", (testimonial_id,))
        if result == 0:
            abort_with_message(404, "Testimonial not found")
        response = MessageResponse(message="Testimonial deleted successfully")
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error deleting testimonial: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error deleting testimonial: {str(e)}")


# ============================================
# ROUTES - VISITOR INFO
# ============================================

@app.route("/api/visitor-info", methods=["POST"])
def create_visitor_info():
    """Create a new visitor info entry from popup modal"""
    try:
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        visitor_data = VisitorInfoCreateSchema(**data)
        
        # Get client IP address
        ip_address = get_client_ip()
        
        query = "INSERT INTO visitor_info (full_name, email, phone, looking_for, ip_address) VALUES (%s, %s, %s, %s, %s)"
        with get_db_cursor() as cursor:
            cursor.execute(query, (
                visitor_data.full_name, visitor_data.email,
                visitor_data.phone, visitor_data.looking_for, ip_address
            ))
            visitor_id = cursor.lastrowid
        
        # Send self-notification email in background
        def send_notification():
            send_self_notification_email(
                "new_visitor",
                "New Website Visitor",
                f"A new visitor has submitted their information through the website popup.",
                {
                    "Visitor Name": visitor_data.full_name,
                    "Visitor Email": visitor_data.email,
                    "Visitor Phone": visitor_data.phone,
                    "Looking For": visitor_data.looking_for or "Not specified",
                    "Visitor ID": visitor_id
                }
            )
        
        thread = threading.Thread(target=send_notification)
        thread.daemon = True
        thread.start()
        
        result = execute_query("SELECT * FROM visitor_info WHERE id = %s", (visitor_id,))
        response = VisitorInfoResponseSchema(**dict(result[0]))
        return jsonify(response.dict()), 201
    except Exception as e:
        print(f"Error creating visitor info: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error creating visitor info: {str(e)}")


@app.route("/api/admin/visitor-info", methods=["GET"])
@require_admin_auth
def get_all_visitor_info():
    """Get all visitor info entries (admin endpoint)"""
    try:
        visitors = execute_query("SELECT * FROM visitor_info ORDER BY created_at DESC")
        result = [VisitorInfoResponseSchema(**dict(v)) for v in visitors]
        return jsonify([r.dict() for r in result])
    except Exception as e:
        print(f"Error fetching visitor info: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching visitor info: {str(e)}")


# ============================================
# ROUTES - LOGS
# ============================================

@app.route("/api/logs", methods=["POST"])
def create_log():
    """Create a new log entry - always returns success even on errors"""
    default_log_type = 'action'
    default_action = 'page_view'
    default_description = ''
    default_user_email = None
    default_ip = None
    default_user_agent = None
    default_metadata = None
    default_created_at = datetime.now()
    
    log_type = default_log_type
    action = default_action
    description = default_description
    user_email = default_user_email
    ip_address = default_ip
    user_agent = default_user_agent
    metadata = default_metadata
    created_at = default_created_at
    
    try:
        ip_address = get_client_ip()
        user_agent = request.headers.get("User-Agent", None)
        
        data = request.get_json()
        if data:
            try:
                log_data = LogCreateSchema(**data)
                log_type = log_data.log_type or default_log_type
                action = log_data.action or default_action
                description = log_data.description or default_description
                user_email = log_data.user_email
                metadata = log_data.metadata
            except Exception:
                pass
        
        query = "INSERT INTO logs (log_type, action, description, user_email, ip_address, user_agent, metadata) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        metadata_json = None
        if metadata:
            try:
                metadata_json = json.dumps(metadata)
            except Exception:
                metadata_json = None
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (
                    log_type, action, description,
                    user_email, ip_address, user_agent, metadata_json
                ))
                log_id = cursor.lastrowid
            
            try:
                result = execute_query("SELECT * FROM logs WHERE id = %s", (log_id,))
                if result and len(result) > 0:
                    log_dict = dict(result[0])
                    
                    if log_dict.get('metadata'):
                        try:
                            if isinstance(log_dict['metadata'], str):
                                log_dict['metadata'] = json.loads(log_dict['metadata'])
                        except:
                            log_dict['metadata'] = None
                    
                    if 'created_at' not in log_dict or log_dict['created_at'] is None:
                        log_dict['created_at'] = datetime.now()
                    
                    response = LogResponseSchema(**log_dict)
                    return jsonify(response.dict())
            except Exception:
                pass
        except Exception:
            pass
    except Exception:
        pass
    
    # Return minimal success response
    try:
        response = LogResponseSchema(
            id=0,
            log_type=log_type,
            action=action,
            description=description,
            user_email=user_email,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata,
            created_at=created_at
        )
        return jsonify(response.dict())
    except Exception:
        return jsonify({
            "id": 0,
            "log_type": "page_view",
            "action": "view",
            "description": "",
            "user_email": None,
            "ip_address": None,
            "user_agent": None,
            "metadata": None,
            "created_at": datetime.now().isoformat()
        })


@app.route("/api/admin/logs", methods=["GET"])
@require_admin_auth
def get_all_logs():
    """Get all logs (admin endpoint)"""
    try:
        log_type = request.args.get('log_type')
        action = request.args.get('action')
        limit = request.args.get('limit', default=100, type=int)
        if limit < 1:
            limit = 100
        if limit > 1000:
            limit = 1000
        
        conditions = []
        params = []
        
        if log_type:
            conditions.append("log_type = %s")
            params.append(log_type)
        
        if action:
            conditions.append("action = %s")
            params.append(action)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        params.append(limit)
        
        query = f"SELECT * FROM logs WHERE {where_clause} ORDER BY created_at DESC LIMIT %s"
        
        logs = execute_query(query, tuple(params))
        
        # Parse JSON metadata
        for log in logs:
            if log.get('metadata'):
                try:
                    log['metadata'] = json.loads(log['metadata'])
                except:
                    log['metadata'] = None
        
        result = [LogResponseSchema(**dict(log)) for log in logs]
        return jsonify([r.dict() for r in result])
    except Exception as e:
        print(f"Error fetching logs: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching logs: {str(e)}")


@app.route("/api/admin/cache-logs", methods=["GET"])
@require_admin_auth
def get_cache_logs():
    """Get cache logs with filtering and pagination (admin endpoint)"""
    try:
        # Get pagination parameters
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=50, type=int)
        
        if page < 1:
            page = 1
        if limit < 1:
            limit = 50
        if limit > 500:
            limit = 500
        
        offset = (page - 1) * limit
        
        # Get filter parameters
        operation_filter = request.args.get('operation')
        status_filter = request.args.get('status')
        search_query = request.args.get('search')
        
        # Build WHERE clause
        conditions = []
        params = []
        
        if operation_filter:
            # Validate operation
            try:
                operation = CacheOperation(operation_filter.lower())
                conditions.append("operation = %s")
                params.append(operation.value)
            except ValueError:
                pass  # Invalid operation, ignore filter
        
        if status_filter:
            # Validate status
            try:
                status = CacheStatus(status_filter.lower())
                conditions.append("status = %s")
                params.append(status.value)
            except ValueError:
                pass  # Invalid status, ignore filter
        
        if search_query:
            # Search in cache_key and cache_type
            conditions.append("(cache_key LIKE %s OR cache_type LIKE %s)")
            search_pattern = f"%{search_query}%"
            params.extend([search_pattern, search_pattern])
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM cache_logs WHERE {where_clause}"
        count_result = execute_query(count_query, tuple(params))
        total = count_result[0]['total'] if count_result else 0
        
        # Calculate pagination
        pages = (total + limit - 1) // limit if limit > 0 else 0
        has_more = page < pages
        
        # Get cache logs
        query = f"""
            SELECT * FROM cache_logs 
            WHERE {where_clause} 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        
        logs = execute_query(query, tuple(params))
        
        # Parse JSON metadata and convert to response schema
        cache_logs = []
        for log in logs:
            # Parse JSON metadata if present
            if log.get('metadata'):
                try:
                    if isinstance(log['metadata'], str):
                        log['metadata'] = json.loads(log['metadata'])
                except (json.JSONDecodeError, TypeError):
                    log['metadata'] = None
            
            # Convert datetime to string if needed
            if log.get('created_at') and isinstance(log['created_at'], datetime):
                log['created_at'] = log['created_at'].isoformat()
            
            # Create response schema
            try:
                cache_log = CacheLogResponseSchema(**dict(log))
                cache_logs.append(cache_log.dict())
            except Exception as e:
                print(f"Error parsing cache log {log.get('id')}: {str(e)}")
                continue
        
        # Return response in expected format
        response_data = CacheLogListResponseSchema(
            success=True,
            logs=cache_logs,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            has_more=has_more
        )
        
        return jsonify(response_data.dict())
        
    except Exception as e:
        print(f"Error fetching cache logs: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching cache logs: {str(e)}")


@app.route("/api/cache-logs", methods=["POST"])
def create_cache_log():
    """Create a new cache log entry - always returns success even on errors"""
    default_cache_key = 'unknown'
    default_operation = CacheOperation.MISS
    default_cache_type = None
    default_response_time_ms = None
    default_cache_size_kb = None
    default_status = CacheStatus.SUCCESS
    default_error_message = None
    default_ip = None
    default_user_agent = None
    default_metadata = None
    default_created_at = datetime.now()
    
    cache_key = default_cache_key
    operation = default_operation
    cache_type = default_cache_type
    response_time_ms = default_response_time_ms
    cache_size_kb = default_cache_size_kb
    status = default_status
    error_message = default_error_message
    ip_address = default_ip
    user_agent = default_user_agent
    metadata = default_metadata
    created_at = default_created_at
    
    try:
        ip_address = get_client_ip()
        user_agent = request.headers.get("User-Agent", None)
        
        data = request.get_json()
        if data:
            try:
                log_data = CacheLogCreateSchema(**data)
                cache_key = log_data.cache_key or default_cache_key
                operation = log_data.operation or default_operation
                cache_type = log_data.cache_type
                response_time_ms = log_data.response_time_ms
                cache_size_kb = log_data.cache_size_kb
                status = log_data.status or default_status
                error_message = log_data.error_message
                metadata = log_data.metadata
            except Exception as e:
                print(f"Error parsing cache log data: {str(e)}")
                # Try to extract basic fields manually
                if isinstance(data, dict):
                    cache_key = data.get('cache_key', default_cache_key)
                    operation_str = data.get('operation', 'miss')
                    try:
                        operation = CacheOperation(operation_str.lower())
                    except ValueError:
                        operation = default_operation
                    cache_type = data.get('cache_type')
                    response_time_ms = data.get('response_time_ms')
                    cache_size_kb = data.get('cache_size_kb')
                    status_str = data.get('status', 'success')
                    try:
                        status = CacheStatus(status_str.lower())
                    except ValueError:
                        status = default_status
                    error_message = data.get('error_message')
                    metadata = data.get('metadata')
        
        query = """INSERT INTO cache_logs 
                   (cache_key, operation, cache_type, response_time_ms, cache_size_kb, 
                    status, error_message, ip_address, user_agent, metadata) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        metadata_json = None
        if metadata:
            try:
                metadata_json = json.dumps(metadata)
            except Exception:
                metadata_json = None
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (
                    cache_key, operation.value, cache_type, response_time_ms, cache_size_kb,
                    status.value, error_message, ip_address, user_agent, metadata_json
                ))
                log_id = cursor.lastrowid
            
            try:
                result = execute_query("SELECT * FROM cache_logs WHERE id = %s", (log_id,))
                if result and len(result) > 0:
                    log_dict = dict(result[0])
                    
                    if log_dict.get('metadata'):
                        try:
                            if isinstance(log_dict['metadata'], str):
                                log_dict['metadata'] = json.loads(log_dict['metadata'])
                        except:
                            log_dict['metadata'] = None
                    
                    if 'created_at' not in log_dict or log_dict['created_at'] is None:
                        log_dict['created_at'] = datetime.now()
                    
                    # Convert enum values to strings
                    if 'operation' in log_dict and isinstance(log_dict['operation'], str):
                        try:
                            log_dict['operation'] = CacheOperation(log_dict['operation'].lower()).value
                        except:
                            pass
                    if 'status' in log_dict and isinstance(log_dict['status'], str):
                        try:
                            log_dict['status'] = CacheStatus(log_dict['status'].lower()).value
                        except:
                            pass
                    
                    response = CacheLogResponseSchema(**log_dict)
                    return jsonify(response.dict())
            except Exception as e:
                print(f"Error fetching created cache log: {str(e)}")
                pass
        except Exception as e:
            print(f"Error inserting cache log: {str(e)}")
            pass
    except Exception as e:
        print(f"Error in create_cache_log: {str(e)}")
        pass
    
    # Return minimal success response
    try:
        response = CacheLogResponseSchema(
            id=0,
            cache_key=cache_key,
            operation=operation,
            cache_type=cache_type,
            response_time_ms=response_time_ms,
            cache_size_kb=cache_size_kb,
            status=status,
            error_message=error_message,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata,
            created_at=created_at
        )
        return jsonify(response.dict())
    except Exception:
        return jsonify({"success": True, "message": "Cache log created"})


@app.route("/api/admin/application-metrics", methods=["GET"])
@require_admin_auth
def get_application_metrics():
    """Get application metrics aggregated by time period"""
    try:
        hours = request.args.get('hours', default=24, type=int)
        if hours < 1:
            hours = 24
        if hours > 168:  # Max 7 days
            hours = 168
        
        # Get metrics aggregated by hour
        query = """
            SELECT 
                DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:00:00') as time_bucket,
                COUNT(*) as request_count,
                AVG(response_time_ms) as avg_response_time,
                MAX(response_time_ms) as max_response_time,
                MIN(response_time_ms) as min_response_time,
                SUM(CASE WHEN is_error = 1 THEN 1 ELSE 0 END) as error_count,
                SUM(CASE WHEN status_code >= 200 AND status_code < 300 THEN 1 ELSE 0 END) as success_count,
                SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as client_error_count,
                SUM(CASE WHEN status_code >= 500 THEN 1 ELSE 0 END) as server_error_count
            FROM application_metrics
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
            GROUP BY time_bucket
            ORDER BY time_bucket ASC
        """
        
        metrics = execute_query(query, (hours,))
        
        # Get current stats (last hour)
        current_query = """
            SELECT 
                COUNT(*) as request_count,
                AVG(response_time_ms) as avg_response_time,
                SUM(CASE WHEN is_error = 1 THEN 1 ELSE 0 END) as error_count,
                SUM(CASE WHEN status_code >= 200 AND status_code < 300 THEN 1 ELSE 0 END) as success_count
            FROM application_metrics
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
        """
        
        current_stats = execute_query(current_query)
        current = current_stats[0] if current_stats and len(current_stats) > 0 else {}
        
        # Get top endpoints by request count
        top_endpoints_query = """
            SELECT 
                endpoint,
                method,
                COUNT(*) as request_count,
                AVG(response_time_ms) as avg_response_time,
                SUM(CASE WHEN is_error = 1 THEN 1 ELSE 0 END) as error_count
            FROM application_metrics
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
            GROUP BY endpoint, method
            ORDER BY request_count DESC
            LIMIT 10
        """
        
        top_endpoints = execute_query(top_endpoints_query, (hours,))
        
        # Get cache statistics from cache_logs
        cache_stats_query = """
            SELECT 
                COUNT(*) as total_cache_ops,
                SUM(CASE WHEN operation = 'hit' THEN 1 ELSE 0 END) as cache_hits,
                SUM(CASE WHEN operation = 'miss' THEN 1 ELSE 0 END) as cache_misses,
                AVG(response_time_ms) as avg_cache_time
            FROM cache_logs
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
        """
        
        cache_stats = execute_query(cache_stats_query, (hours,))
        cache_data = cache_stats[0] if cache_stats and len(cache_stats) > 0 else {}
        
        # Calculate cache hit rate
        total_cache_ops = cache_data.get('total_cache_ops', 0) or 0
        cache_hits = cache_data.get('cache_hits', 0) or 0
        cache_hit_rate = (cache_hits / total_cache_ops * 100) if total_cache_ops > 0 else 0
        
        # Get system metrics (CPU, RAM, Bandwidth)
        system_metrics_query = """
            SELECT 
                cpu_usage,
                ram_usage,
                ram_used_mb,
                ram_total_mb,
                bandwidth_in_mb,
                bandwidth_out_mb,
                bandwidth_total_mb,
                created_at
            FROM system_metrics
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
            ORDER BY created_at ASC
        """
        
        system_metrics = execute_query(system_metrics_query, (hours,))
        
        # Get current system metrics (most recent)
        current_system_query = """
            SELECT 
                cpu_usage,
                ram_usage,
                ram_used_mb,
                ram_total_mb,
                bandwidth_in_mb,
                bandwidth_out_mb,
                bandwidth_total_mb
            FROM system_metrics
            ORDER BY created_at DESC
            LIMIT 1
        """
        
        current_system = execute_query(current_system_query)
        current_system_data = current_system[0] if current_system and len(current_system) > 0 else {}
        
        # Format system metrics time series
        system_time_series = []
        for sm in system_metrics:
            created_at = sm.get('created_at')
            if isinstance(created_at, datetime):
                time_str = created_at.strftime('%Y-%m-%d %H:00:00')
            else:
                time_str = str(created_at)
            
            system_time_series.append({
                "time": time_str,
                "cpu_usage": float(sm.get('cpu_usage', 0) or 0),
                "ram_usage": float(sm.get('ram_usage', 0) or 0),
                "ram_used_mb": float(sm.get('ram_used_mb', 0) or 0),
                "ram_total_mb": float(sm.get('ram_total_mb', 0) or 0),
                "bandwidth_in_mb": float(sm.get('bandwidth_in_mb', 0) or 0),
                "bandwidth_out_mb": float(sm.get('bandwidth_out_mb', 0) or 0),
                "bandwidth_total_mb": float(sm.get('bandwidth_total_mb', 0) or 0)
            })
        
        return jsonify({
            "success": True,
            "time_series": [
                {
                    "time": m.get('time_bucket', ''),
                    "request_count": int(m.get('request_count', 0) or 0),
                    "avg_response_time": float(m.get('avg_response_time', 0) or 0),
                    "max_response_time": float(m.get('max_response_time', 0) or 0),
                    "min_response_time": float(m.get('min_response_time', 0) or 0),
                    "error_count": int(m.get('error_count', 0) or 0),
                    "success_count": int(m.get('success_count', 0) or 0),
                    "client_error_count": int(m.get('client_error_count', 0) or 0),
                    "server_error_count": int(m.get('server_error_count', 0) or 0)
                }
                for m in metrics
            ],
            "current": {
                "request_count": int(current.get('request_count', 0) or 0),
                "avg_response_time": float(current.get('avg_response_time', 0) or 0),
                "error_count": int(current.get('error_count', 0) or 0),
                "success_count": int(current.get('success_count', 0) or 0)
            },
            "top_endpoints": [
                {
                    "endpoint": e.get('endpoint', ''),
                    "method": e.get('method', ''),
                    "request_count": int(e.get('request_count', 0) or 0),
                    "avg_response_time": float(e.get('avg_response_time', 0) or 0),
                    "error_count": int(e.get('error_count', 0) or 0)
                }
                for e in top_endpoints
            ],
            "cache_stats": {
                "total_operations": int(total_cache_ops),
                "cache_hits": int(cache_hits),
                "cache_misses": int(cache_data.get('cache_misses', 0) or 0),
                "cache_hit_rate": round(cache_hit_rate, 2),
                "avg_cache_time": float(cache_data.get('avg_cache_time', 0) or 0)
            },
            "system_metrics": {
                "time_series": system_time_series,
                "current": {
                    "cpu_usage": float(current_system_data.get('cpu_usage', 0) or 0),
                    "ram_usage": float(current_system_data.get('ram_usage', 0) or 0),
                    "ram_used_mb": float(current_system_data.get('ram_used_mb', 0) or 0),
                    "ram_total_mb": float(current_system_data.get('ram_total_mb', 0) or 0),
                    "bandwidth_in_mb": float(current_system_data.get('bandwidth_in_mb', 0) or 0),
                    "bandwidth_out_mb": float(current_system_data.get('bandwidth_out_mb', 0) or 0),
                    "bandwidth_total_mb": float(current_system_data.get('bandwidth_total_mb', 0) or 0)
                }
            }
        })
        
    except Exception as e:
        print(f"Error fetching application metrics: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching application metrics: {str(e)}")


# ============================================
# ROUTES - BLOGS
# ============================================

@app.route("/api/blogs", methods=["GET"])
def get_blogs():
    """Get all blogs with filtering and pagination"""
    try:
        pagination = get_pagination_params()
        offset = (pagination.page - 1) * pagination.limit
        
        category = request.args.get('category')
        is_featured = request.args.get('is_featured', type=lambda x: x.lower() == 'true' if x else None)
        is_active = request.args.get('is_active', type=lambda x: x.lower() == 'true' if x else None)
        
        conditions = []
        params = []
        
        if is_active is not None:
            is_active_int = 1 if is_active else 0
            conditions.append("is_active = %s")
            params.append(is_active_int)
        
        if category:
            conditions.append("category = %s")
            params.append(category)
        
        if is_featured is not None:
            is_featured_int = 1 if is_featured else 0
            conditions.append("is_featured = %s")
            params.append(is_featured_int)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        count_query = f"SELECT COUNT(*) as total FROM blogs WHERE {where_clause}"
        total_result = execute_query(count_query, tuple(params))
        total = total_result[0]['total'] if total_result else 0
        
        query = f"SELECT * FROM blogs WHERE {where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
        params.extend([pagination.limit, offset])
        
        blogs = execute_query(query, tuple(params))
        
        blog_list = []
        for blog in blogs:
            blog_dict = dict(blog)
            if blog_dict.get('tags'):
                try:
                    if isinstance(blog_dict['tags'], str):
                        blog_dict['tags'] = json.loads(blog_dict['tags'])
                    elif not isinstance(blog_dict['tags'], list):
                        blog_dict['tags'] = []
                except:
                    blog_dict['tags'] = []
            else:
                blog_dict['tags'] = []
            if 'image_url' in blog_dict and blog_dict['image_url']:
                blog_dict['image_url'] = normalize_image_url(blog_dict['image_url'])
            blog_list.append(blog_dict)
        
        response = PaginatedResponse(
            total=total,
            page=pagination.page,
            limit=pagination.limit,
            pages=calculate_pages(total, pagination.limit),
            items=blog_list
        )
        return jsonify(response.dict())
    except Exception as e:
        traceback.print_exc()
        abort_with_message(500, f"Failed to fetch blogs: {str(e)}")


@app.route("/api/blogs/<int:blog_id>", methods=["GET"])
def get_blog(blog_id: int):
    """Get a single blog by ID"""
    try:
        blog_query = "SELECT * FROM blogs WHERE id = %s"
        blogs = execute_query(blog_query, (blog_id,))
        
        if not blogs:
            abort_with_message(404, "Blog not found")
        
        blog_data = dict(blogs[0])
        
        if blog_data.get('tags'):
            try:
                if isinstance(blog_data['tags'], str):
                    blog_data['tags'] = json.loads(blog_data['tags'])
                elif not isinstance(blog_data['tags'], list):
                    blog_data['tags'] = []
            except:
                blog_data['tags'] = []
        else:
            blog_data['tags'] = []
        
        if 'image_url' in blog_data and blog_data['image_url']:
            blog_data['image_url'] = normalize_image_url(blog_data['image_url'])
        
        response = BlogResponseSchema(**blog_data)
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error fetching blog: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching blog: {str(e)}")


@app.route("/api/blogs", methods=["POST"])
@require_admin_auth
def create_blog():
    """Create a new blog"""
    try:
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        blog_data = BlogCreateSchema(**data)
        
        tags_json = json.dumps(blog_data.tags) if blog_data.tags else None
        
        insert_query = """
            INSERT INTO blogs (
                title, excerpt, content, category, tags, image_url, 
                author, views, is_featured, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        with get_db_cursor() as cursor:
            cursor.execute(insert_query, (
                blog_data.title,
                blog_data.excerpt,
                blog_data.content,
                blog_data.category,
                tags_json,
                blog_data.image_url,
                blog_data.author or 'Tirumakudalu Properties',
                blog_data.views,
                blog_data.is_featured,
                blog_data.is_active
            ))
            blog_id = cursor.lastrowid
        
        # Return the created blog
        blog_query = "SELECT * FROM blogs WHERE id = %s"
        blogs = execute_query(blog_query, (blog_id,))
        blog_data_dict = dict(blogs[0])
        
        if blog_data_dict.get('tags'):
            try:
                if isinstance(blog_data_dict['tags'], str):
                    blog_data_dict['tags'] = json.loads(blog_data_dict['tags'])
                elif not isinstance(blog_data_dict['tags'], list):
                    blog_data_dict['tags'] = []
            except:
                blog_data_dict['tags'] = []
        else:
            blog_data_dict['tags'] = []
        
        if 'image_url' in blog_data_dict and blog_data_dict['image_url']:
            blog_data_dict['image_url'] = normalize_image_url(blog_data_dict['image_url'])
        
        response = BlogResponseSchema(**blog_data_dict)
        return jsonify(response.dict()), 201
    except Exception as e:
        print(f"Error creating blog: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error creating blog: {str(e)}")


@app.route("/api/blogs/<int:blog_id>", methods=["PUT"])
@require_admin_auth
def update_blog(blog_id: int):
    """Update a blog"""
    try:
        existing = execute_query("SELECT id FROM blogs WHERE id = %s", (blog_id,))
        if not existing:
            abort_with_message(404, "Blog not found")
        
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        blog_data = BlogUpdateSchema(**data)
        
        updates = []
        params = []
        
        if blog_data.title is not None:
            updates.append("title = %s")
            params.append(blog_data.title)
        if blog_data.excerpt is not None:
            updates.append("excerpt = %s")
            params.append(blog_data.excerpt)
        if blog_data.content is not None:
            updates.append("content = %s")
            params.append(blog_data.content)
        if blog_data.category is not None:
            updates.append("category = %s")
            params.append(blog_data.category)
        if blog_data.tags is not None:
            updates.append("tags = %s")
            tags_json = json.dumps(blog_data.tags)
            params.append(tags_json)
        if blog_data.image_url is not None:
            updates.append("image_url = %s")
            params.append(blog_data.image_url)
        if blog_data.author is not None:
            updates.append("author = %s")
            params.append(blog_data.author)
        if blog_data.views is not None:
            updates.append("views = %s")
            params.append(blog_data.views)
        if blog_data.is_featured is not None:
            updates.append("is_featured = %s")
            params.append(blog_data.is_featured)
        if blog_data.is_active is not None:
            updates.append("is_active = %s")
            params.append(blog_data.is_active)
        
        if not updates:
            blog_query = "SELECT * FROM blogs WHERE id = %s"
            blogs = execute_query(blog_query, (blog_id,))
            blog_data_dict = dict(blogs[0])
            if blog_data_dict.get('tags'):
                try:
                    if isinstance(blog_data_dict['tags'], str):
                        blog_data_dict['tags'] = json.loads(blog_data_dict['tags'])
                except:
                    blog_data_dict['tags'] = []
            response = BlogResponseSchema(**blog_data_dict)
            return jsonify(response.dict())
        
        params.append(blog_id)
        update_query = f"UPDATE blogs SET {', '.join(updates)} WHERE id = %s"
        execute_update(update_query, tuple(params))
        
        # Return updated blog
        blog_query = "SELECT * FROM blogs WHERE id = %s"
        blogs = execute_query(blog_query, (blog_id,))
        blog_data_dict = dict(blogs[0])
        if blog_data_dict.get('tags'):
            try:
                if isinstance(blog_data_dict['tags'], str):
                    blog_data_dict['tags'] = json.loads(blog_data_dict['tags'])
            except:
                blog_data_dict['tags'] = []
        if 'image_url' in blog_data_dict and blog_data_dict['image_url']:
            blog_data_dict['image_url'] = normalize_image_url(blog_data_dict['image_url'])
        
        response = BlogResponseSchema(**blog_data_dict)
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error updating blog: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error updating blog: {str(e)}")


@app.route("/api/blogs/<int:blog_id>", methods=["DELETE"])
@require_admin_auth
def delete_blog(blog_id: int):
    """Delete a blog"""
    try:
        existing = execute_query("SELECT id FROM blogs WHERE id = %s", (blog_id,))
        if not existing:
            abort_with_message(404, "Blog not found")
        
        delete_query = "DELETE FROM blogs WHERE id = %s"
        execute_update(delete_query, (blog_id,))
        
        response = MessageResponse(message="Blog deleted successfully")
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error deleting blog: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error deleting blog: {str(e)}")


# ============================================
# ROUTES - CONTACT INQUIRIES
# ============================================

@app.route("/api/admin/inquiries", methods=["GET"])
@require_admin_auth
def get_inquiries():
    """Get all contact inquiries (admin endpoint)"""
    try:
        status_str = request.args.get('status')
        status = None
        if status_str:
            try:
                status = InquiryStatus(status_str)
            except ValueError:
                pass
        
        if status:
            query = "SELECT * FROM contact_inquiries WHERE status = %s ORDER BY created_at DESC"
            inquiries = execute_query(query, (status.value,))
        else:
            query = "SELECT * FROM contact_inquiries ORDER BY created_at DESC"
            inquiries = execute_query(query)
        
        result = [ContactInquiryResponseSchema(**dict(i)) for i in inquiries]
        return jsonify([r.dict() for r in result])
    except Exception as e:
        print(f"Error fetching inquiries: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching inquiries: {str(e)}")


@app.route("/api/contact", methods=["POST"])
def create_inquiry():
    """Create a new contact inquiry"""
    try:
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        inquiry_data = ContactInquiryCreateSchema(**data)
        
        # Get client IP address
        ip_address = get_client_ip()
        
        query = """
            INSERT INTO contact_inquiries (name, email, subject, message, phone, property_id, status, ip_address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (
                inquiry_data.name, inquiry_data.email, inquiry_data.subject,
                inquiry_data.message, inquiry_data.phone, inquiry_data.property_id,
                InquiryStatus.NEW.value, ip_address
            ))
            inquiry_id = cursor.lastrowid
        
        # Send email notification if this is a Schedule Visit request
        if inquiry_data.subject and inquiry_data.subject.lower() == "schedule visit":
            visit_date, visit_time, additional_notes = parse_visit_details_from_message(inquiry_data.message)
            
            def send_email():
                send_schedule_visit_email(
                    inquiry_data.name,
                    inquiry_data.email,
                    inquiry_data.phone,
                    visit_date,
                    visit_time,
                    inquiry_data.message,
                    inquiry_data.property_id
                )
            
            thread = threading.Thread(target=send_email)
            thread.daemon = True
            thread.start()
        
        # Send self-notification email for all contact inquiries
        def send_notification():
            property_title = ""
            if inquiry_data.property_id:
                try:
                    # Check residential_properties first
                    properties = execute_query("SELECT property_name as title FROM residential_properties WHERE id = %s", (inquiry_data.property_id,))
                    if not properties or len(properties) == 0:
                        # Check plot_properties if not found in residential
                        properties = execute_query("SELECT project_name as title FROM plot_properties WHERE id = %s", (inquiry_data.property_id,))
                    if properties and len(properties) > 0:
                        property_title = properties[0]['title']
                except Exception:
                    pass
            
            if inquiry_data.subject and inquiry_data.subject.lower() == "schedule visit":
                notification_title = "New Schedule Visit Request"
                notification_message = f"A new schedule visit request has been received from {inquiry_data.name}. Please check your dashboard to manage this request."
            else:
                notification_title = "New Contact Inquiry"
                notification_message = f"A new contact inquiry has been received from {inquiry_data.name}. Please check your dashboard to respond."
            
            send_self_notification_email(
                "new_inquiry",
                notification_title,
                notification_message,
                {
                    "Inquirer Name": inquiry_data.name,
                    "Inquirer Email": inquiry_data.email,
                    "Inquirer Phone": inquiry_data.phone or "Not provided",
                    "Subject": inquiry_data.subject or "No subject",
                    "Property": property_title or "General inquiry",
                    "Inquiry ID": inquiry_id,
                    "Status": "New"
                }
            )
        
        thread = threading.Thread(target=send_notification)
        thread.daemon = True
        thread.start()
        
        result = execute_query("SELECT * FROM contact_inquiries WHERE id = %s", (inquiry_id,))
        response = ContactInquiryResponseSchema(**dict(result[0]))
        return jsonify(response.dict()), 201
    except Exception as e:
        print(f"Error creating inquiry: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error creating inquiry: {str(e)}")


@app.route("/api/admin/inquiries/<int:inquiry_id>", methods=["PUT"])
@require_admin_auth
def update_inquiry(inquiry_id: int):
    """Update a contact inquiry"""
    try:
        existing = execute_query("SELECT id FROM contact_inquiries WHERE id = %s", (inquiry_id,))
        if not existing:
            abort_with_message(404, "Inquiry not found")
        
        data = request.get_json()
        if not data:
            abort_with_message(400, "Invalid request data")
        
        inquiry_data = ContactInquiryUpdateSchema(**data)
        
        updates = []
        params = []
        
        if inquiry_data.name is not None:
            updates.append("name = %s")
            params.append(inquiry_data.name)
        if inquiry_data.email is not None:
            updates.append("email = %s")
            params.append(inquiry_data.email)
        if inquiry_data.subject is not None:
            updates.append("subject = %s")
            params.append(inquiry_data.subject)
        if inquiry_data.message is not None:
            updates.append("message = %s")
            params.append(inquiry_data.message)
        if inquiry_data.phone is not None:
            updates.append("phone = %s")
            params.append(inquiry_data.phone)
        if inquiry_data.property_id is not None:
            updates.append("property_id = %s")
            params.append(inquiry_data.property_id)
        if inquiry_data.status is not None:
            updates.append("status = %s")
            params.append(inquiry_data.status.value)
        
        if updates:
            params.append(inquiry_id)
            update_query = f"UPDATE contact_inquiries SET {', '.join(updates)} WHERE id = %s"
            execute_update(update_query, tuple(params))
        
        result = execute_query("SELECT * FROM contact_inquiries WHERE id = %s", (inquiry_id,))
        response = ContactInquiryResponseSchema(**dict(result[0]))
        return jsonify(response.dict())
    except Exception as e:
        print(f"Error updating inquiry: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error updating inquiry: {str(e)}")


# ============================================
# ROUTES - STATISTICS
# ============================================

# Simple in-memory cache for stats (TTL: 60 seconds)
_stats_cache = {}
_stats_cache_ttl = 60  # Cache for 60 seconds

def get_cached_stats(cache_key):
    """Get cached stats if available and not expired"""
    if cache_key in _stats_cache:
        cached_data, timestamp = _stats_cache[cache_key]
        if time.time() - timestamp < _stats_cache_ttl:
            return cached_data
        else:
            # Remove expired cache
            del _stats_cache[cache_key]
    return None

def set_cached_stats(cache_key, data):
    """Cache stats data with current timestamp"""
    _stats_cache[cache_key] = (data, time.time())

@app.route("/api/stats/properties", methods=["GET"])
def get_property_stats():
    """Get property statistics (optimized with single query and caching)"""
    try:
        # Check cache first
        cache_key = "property_stats"
        cached_result = get_cached_stats(cache_key)
        if cached_result:
            return jsonify(cached_result)
        
        # Query both residential_properties and plot_properties
        query = f"""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = '{PropertyStatus.SALE.value}' THEN 1 ELSE 0 END) as for_sale,
                SUM(CASE WHEN status = '{PropertyStatus.RENT.value}' THEN 1 ELSE 0 END) as for_rent,
                SUM(CASE WHEN is_featured = 1 THEN 1 ELSE 0 END) as featured
            FROM (
                SELECT status, is_featured FROM residential_properties WHERE is_active = 1
                UNION ALL
                SELECT status, is_featured FROM plot_properties WHERE is_active = 1
            ) as combined
        """
        
        stats_result = execute_query(query)
        total = 0
        for_sale = 0
        for_rent = 0
        featured = 0
        
        if stats_result and len(stats_result) > 0 and stats_result[0]:
            total = int(stats_result[0].get('total', 0) or 0)
            for_sale = int(stats_result[0].get('for_sale', 0) or 0)
            for_rent = int(stats_result[0].get('for_rent', 0) or 0)
            featured = int(stats_result[0].get('featured', 0) or 0)
        
        # Get type breakdown from both tables
        by_type = {}
        try:
            type_stats_res = execute_query("SELECT type, COUNT(*) as count FROM residential_properties WHERE is_active = 1 GROUP BY type")
            type_stats_plot = execute_query("SELECT 'plot' as type, COUNT(*) as count FROM plot_properties WHERE is_active = 1")
            
            if type_stats_res:
                for row in type_stats_res:
                    if row and row.get('type') is not None:
                        type_name = str(row.get('type', ''))
                        count_val = row.get('count', 0)
                        by_type[type_name] = int(count_val or 0)
            
            if type_stats_plot:
                for row in type_stats_plot:
                    if row and row.get('count', 0) > 0:
                        by_type['plot'] = by_type.get('plot', 0) + int(row.get('count', 0))
        except Exception as e:
            print(f"Error fetching property types: {str(e)}")
        
        result = PropertyStatsSchema(
            total=int(total or 0),
            for_sale=int(for_sale or 0),
            for_rent=int(for_rent or 0),
            by_type=by_type if by_type else {},
            featured=int(featured or 0)
        )
        
        result_dict = result.dict()
        # Cache the result
        set_cached_stats(cache_key, result_dict)
        
        return jsonify(result_dict)
    except Exception as e:
        print(f"Error fetching property stats: {str(e)}")
        traceback.print_exc()
        result = PropertyStatsSchema(total=0, for_sale=0, for_rent=0, by_type={}, featured=0)
        return jsonify(result.dict())


@app.route("/api/stats/frontend", methods=["GET"])
def get_frontend_stats():
    """Get frontend statistics for homepage (with caching)"""
    try:
        # Check cache first
        cache_key = "frontend_stats"
        cached_result = get_cached_stats(cache_key)
        if cached_result:
            return jsonify(cached_result)
        
        # Optimized: Use single query with conditional aggregation where possible
        def get_count(query):
            try:
                result = execute_query(query)
                return result[0]['count'] if result and len(result) > 0 else 0
            except Exception as e:
                print(f"Error executing query: {query}, Error: {str(e)}")
                return 0
        
        properties_listed = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties WHERE is_active = 1 UNION ALL SELECT id FROM plot_properties WHERE is_active = 1) as combined")
        happy_clients = get_count("SELECT COUNT(*) as count FROM testimonials WHERE is_approved = 1")
        if happy_clients == 0:
            happy_clients = get_count("SELECT COUNT(*) as count FROM contact_inquiries")
        
        years_experience = 15
        
        deals_closed = get_count("SELECT COUNT(*) as count FROM contact_inquiries WHERE status = 'closed'")
        if deals_closed == 0:
            deals_closed = get_count("SELECT COUNT(*) as count FROM contact_inquiries")
        
        result = FrontendStatsSchema(
            properties_listed=properties_listed,
            happy_clients=happy_clients,
            years_experience=years_experience,
            deals_closed=deals_closed
        )
        
        result_dict = result.dict()
        # Cache the result
        set_cached_stats(cache_key, result_dict)
        
        return jsonify(result_dict)
    except Exception as e:
        print(f"Error in get_frontend_stats: {str(e)}")
        result = FrontendStatsSchema(properties_listed=0, happy_clients=0, years_experience=15, deals_closed=0)
        return jsonify(result.dict())


# ============================================
# ROUTES - SYSTEM METRICS (Monitoring)
# ============================================

# Track bandwidth for this application
_app_bandwidth_in = 0
_app_bandwidth_out = 0
_bandwidth_lock = threading.Lock()

def track_bandwidth(response_size):
    """Track bandwidth usage for this application"""
    global _app_bandwidth_in, _app_bandwidth_out
    with _bandwidth_lock:
        _app_bandwidth_out += response_size / (1024 * 1024)  # Convert to MB

@app.after_request
def after_request(response):
    """Track bandwidth after each request"""
    try:
        if hasattr(response, 'content_length') and response.content_length:
            track_bandwidth(response.content_length)
    except:
        pass
    return response

@app.route("/api/admin/metrics/collect", methods=["POST"])
@require_admin_auth
def collect_metrics():
    """Collect and store system metrics in both permanent and temporary tables"""
    try:
        # Create system_metrics table if it doesn't exist (permanent storage for graphs)
        # Note: These metrics track the APPLICATION PROCESS only, not the entire system
        create_system_table_query = """
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'Application process CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'Application process RAM usage percentage (of system total)',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'Application process RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Total system RAM in MB (for percentage calculation)',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Application bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Application bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Total application bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_system_table_query)
        except Exception as table_error:
            print(f"Warning: Could not create system_metrics table: {str(table_error)}")
            traceback.print_exc()
            # Continue anyway - table might already exist
        
        # Create temporary_metrics table if it doesn't exist (temporary storage for stat cards)
        # Note: These metrics track the APPLICATION PROCESS only, not the entire system
        create_temp_table_query = """
            CREATE TABLE IF NOT EXISTS temporary_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'Application process CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'Application process RAM usage percentage (of system total)',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'Application process RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Total system RAM in MB (for percentage calculation)',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Application bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Application bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Total application bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_temp_table_query)
        except Exception as table_error:
            print(f"Warning: Could not create temporary_metrics table: {str(table_error)}")
            traceback.print_exc()
            # Continue anyway - table might already exist
        
        # Initialize default values
        cpu_percent = 0.0
        ram_percent = 0.0
        ram_used_mb = 0.0
        ram_total_mb = 0.0
        
        # Try to get CPU and RAM usage for THIS APPLICATION PROCESS ONLY (not system-wide)
        # Handle cases where psutil is not available or fails
        try:
            # Check if psutil is available
            if psutil is None:
                raise ImportError("psutil module is not available")
            
            # Get the current process (this Flask application)
            current_process = psutil.Process(os.getpid())
            
            # Get CPU usage for this process only
            try:
                # Get CPU usage for this process (percentage of a single CPU core)
                # If multiprocessor, this can exceed 100% (e.g., 200% = 2 cores at 100%)
                cpu_percent = current_process.cpu_percent(interval=0.1)
                if cpu_percent is None:
                    cpu_percent = 0.0
                # Normalize to percentage (divide by number of CPU cores to get 0-100%)
                num_cores = psutil.cpu_count() or 1
                cpu_percent = min(100.0, (cpu_percent / num_cores) * 100) if num_cores > 0 else cpu_percent
            except Exception as cpu_error:
                print(f"Warning: Could not get process CPU usage: {str(cpu_error)}")
                cpu_percent = 0.0
            
            # Get RAM usage for this process only
            try:
                process_memory = current_process.memory_info()
                ram_used_mb = process_memory.rss / (1024 * 1024)  # RSS = Resident Set Size (actual RAM used)
                
                # Get total system RAM to calculate percentage
                system_memory = psutil.virtual_memory()
                ram_total_mb = system_memory.total / (1024 * 1024)
                ram_percent = (ram_used_mb / ram_total_mb * 100) if ram_total_mb > 0 else 0.0
            except Exception as ram_error:
                print(f"Warning: Could not get process RAM usage: {str(ram_error)}")
                ram_percent = 0.0
                ram_used_mb = 0.0
                ram_total_mb = 0.0
                
        except ImportError as import_error:
            error_msg = f"psutil module not available: {str(import_error)}. Please install psutil: pip install psutil"
            print(f"Error: {error_msg}")
            traceback.print_exc()
            return jsonify({
                "success": False,
                "error": "System metrics collection unavailable. psutil module is not installed. Please install it: pip install psutil",
                "details": str(import_error)
            }), 500
        except Exception as psutil_error:
            error_msg = f"Error accessing system resources: {str(psutil_error)}"
            print(f"Warning: {error_msg}")
            traceback.print_exc()
            # Continue with default values (0.0) - don't fail the request
        
        # Get bandwidth for this application
        try:
            with _bandwidth_lock:
                bandwidth_in = _app_bandwidth_in
                bandwidth_out = _app_bandwidth_out
                bandwidth_total = bandwidth_in + bandwidth_out
                # Reset counters after reading
                _app_bandwidth_in = 0
                _app_bandwidth_out = 0
        except Exception as bandwidth_error:
            print(f"Warning: Could not get bandwidth metrics: {str(bandwidth_error)}")
            bandwidth_in = 0.0
            bandwidth_out = 0.0
            bandwidth_total = 0.0
        
        # Store metrics in both tables (permanent and temporary)
        try:
            # Insert into system_metrics (permanent storage for graphs)
            insert_system_query = """
                INSERT INTO system_metrics 
                (cpu_usage, ram_usage, ram_used_mb, ram_total_mb, 
                 bandwidth_in_mb, bandwidth_out_mb, bandwidth_total_mb)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            execute_update(
                insert_system_query,
                (cpu_percent, ram_percent, ram_used_mb, ram_total_mb,
                 bandwidth_in, bandwidth_out, bandwidth_total)
            )
            
            # Insert into temporary_metrics (temporary storage for stat cards)
            insert_temp_query = """
                INSERT INTO temporary_metrics 
                (cpu_usage, ram_usage, ram_used_mb, ram_total_mb, 
                 bandwidth_in_mb, bandwidth_out_mb, bandwidth_total_mb)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            execute_update(
                insert_temp_query,
                (cpu_percent, ram_percent, ram_used_mb, ram_total_mb,
                 bandwidth_in, bandwidth_out, bandwidth_total)
            )
        except Exception as db_error:
            error_msg = f"Database error storing metrics: {str(db_error)}"
            print(f"Error: {error_msg}")
            traceback.print_exc()
            return jsonify({
                "success": False,
                "error": "Failed to store metrics in database",
                "details": str(db_error)
            }), 500
        
        # Cleanup old data from system_metrics (keep only last 1000 records)
        # Use a more compatible approach for MySQL
        try:
            # Count total records
            count_query = "SELECT COUNT(*) as total FROM system_metrics"
            count_result = execute_query(count_query)
            total_records = count_result[0]['total'] if count_result else 0
            
            # Only cleanup if we have more than 1000 records
            if total_records > 1000:
                # Get the IDs to keep (last 1000)
                keep_ids_query = """
                    SELECT id FROM system_metrics 
                    ORDER BY created_at DESC 
                    LIMIT 1000
                """
                keep_ids = execute_query(keep_ids_query)
                
                if keep_ids:
                    keep_id_list = [row['id'] for row in keep_ids]
                    if keep_id_list:
                        # Use parameterized query for safety
                        placeholders = ','.join(['%s'] * len(keep_id_list))
                        cleanup_query = f"""
                            DELETE FROM system_metrics 
                            WHERE id NOT IN ({placeholders})
                        """
                        execute_update(cleanup_query, tuple(keep_id_list))
        except Exception as e:
            print(f"Error cleaning up old system_metrics: {e}")
            traceback.print_exc()
            # Don't fail the whole request if cleanup fails
        
        # Cleanup old data from temporary_metrics (keep only last 5 minutes)
        try:
            cleanup_temp_query = """
                DELETE FROM temporary_metrics 
                WHERE created_at < DATE_SUB(NOW(), INTERVAL 5 MINUTE)
            """
            deleted_count = execute_update(cleanup_temp_query)
            if deleted_count > 0:
                print(f"Cleaned up {deleted_count} old records from temporary_metrics")
        except Exception as e:
            print(f"Error cleaning up old temporary_metrics: {e}")
            traceback.print_exc()
            # Don't fail the whole request if cleanup fails
        
        return jsonify({
            "success": True,
            "message": "Metrics collected successfully",
            "metrics": {
                "cpu_usage": cpu_percent,
                "ram_usage": ram_percent,
                "ram_used_mb": round(ram_used_mb, 2),
                "ram_total_mb": round(ram_total_mb, 2),
                "bandwidth_in_mb": round(bandwidth_in, 2),
                "bandwidth_out_mb": round(bandwidth_out, 2),
                "bandwidth_total_mb": round(bandwidth_total, 2)
            }
        })
    except Exception as e:
        error_msg = f"Error collecting metrics: {str(e)}"
        print(f"Error: {error_msg}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": "Failed to collect system metrics",
            "details": str(e)
        }), 500

@app.route("/api/admin/metrics/collect-app", methods=["POST"])
def collect_app_metrics():
    """Collect and store frontend application-specific metrics (CPU, RAM, Bandwidth)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Extract metrics from request
        cpu_usage = float(data.get('cpu_usage', 0))
        ram_usage = float(data.get('ram_usage', 0))
        ram_used_mb = float(data.get('ram_used_mb', 0))
        ram_total_mb = float(data.get('ram_total_mb', 0))
        bandwidth_in_mb = float(data.get('bandwidth_in_mb', 0))
        bandwidth_out_mb = float(data.get('bandwidth_out_mb', 0))
        bandwidth_total_mb = float(data.get('bandwidth_total_mb', 0))
        
        # Validate values
        cpu_usage = max(0, min(100, cpu_usage))
        ram_usage = max(0, min(100, ram_usage))
        ram_used_mb = max(0, ram_used_mb)
        ram_total_mb = max(0, ram_total_mb)
        bandwidth_in_mb = max(0, bandwidth_in_mb)
        bandwidth_out_mb = max(0, bandwidth_out_mb)
        bandwidth_total_mb = max(0, bandwidth_total_mb)
        
        # Create application_metrics table if it doesn't exist
        create_app_metrics_table_query = """
            CREATE TABLE IF NOT EXISTS application_metrics_frontend (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'Frontend application CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'Frontend application RAM usage percentage',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'Frontend application RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Frontend application total RAM in MB',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Frontend application bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Frontend application bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Frontend application total bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_app_metrics_table_query)
        except Exception as table_error:
            print(f"Warning: Could not create application_metrics_frontend table: {str(table_error)}")
            traceback.print_exc()
        
        # Store metrics in database
        try:
            insert_query = """
                INSERT INTO application_metrics_frontend 
                (cpu_usage, ram_usage, ram_used_mb, ram_total_mb, 
                 bandwidth_in_mb, bandwidth_out_mb, bandwidth_total_mb)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            execute_update(
                insert_query,
                (cpu_usage, ram_usage, ram_used_mb, ram_total_mb,
                 bandwidth_in_mb, bandwidth_out_mb, bandwidth_total_mb)
            )
        except Exception as db_error:
            error_msg = f"Database error storing frontend application metrics: {str(db_error)}"
            print(f"Error: {error_msg}")
            traceback.print_exc()
            return jsonify({
                "success": False,
                "error": "Failed to store metrics in database",
                "details": str(db_error)
            }), 500
        
        # Cleanup old data (keep only last 1000 records)
        try:
            count_query = "SELECT COUNT(*) as total FROM application_metrics_frontend"
            count_result = execute_query(count_query)
            total_records = count_result[0]['total'] if count_result else 0
            
            if total_records > 1000:
                keep_ids_query = """
                    SELECT id FROM application_metrics_frontend 
                    ORDER BY created_at DESC 
                    LIMIT 1000
                """
                keep_ids = execute_query(keep_ids_query)
                
                if keep_ids:
                    keep_id_list = [row['id'] for row in keep_ids]
                    if keep_id_list:
                        placeholders = ','.join(['%s'] * len(keep_id_list))
                        cleanup_query = f"""
                            DELETE FROM application_metrics_frontend 
                            WHERE id NOT IN ({placeholders})
                        """
                        execute_update(cleanup_query, tuple(keep_id_list))
        except Exception as e:
            print(f"Error cleaning up old application_metrics_frontend: {e}")
            # Don't fail the whole request if cleanup fails
        
        return jsonify({
            "success": True,
            "message": "Frontend application metrics collected successfully",
            "metrics": {
                "cpu_usage": cpu_usage,
                "ram_usage": ram_usage,
                "ram_used_mb": ram_used_mb,
                "ram_total_mb": ram_total_mb,
                "bandwidth_in_mb": bandwidth_in_mb,
                "bandwidth_out_mb": bandwidth_out_mb,
                "bandwidth_total_mb": bandwidth_total_mb
            }
        })
        
    except Exception as e:
        error_msg = f"Error collecting frontend application metrics: {str(e)}"
        print(f"Error: {error_msg}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": "Failed to collect frontend application metrics",
            "details": str(e)
        }), 500

@app.route("/api/admin/metrics", methods=["GET"])
@require_admin_auth
def get_metrics():
    """Get system metrics for display"""
    try:
        # Get time range (default: last 24 hours)
        hours = request.args.get('hours', type=int, default=24)
        limit = request.args.get('limit', type=int, default=100)
        
        # Validate inputs
        if hours < 1:
            hours = 24
        if limit < 1 or limit > 1000:
            limit = 100
        
        # Create system_metrics table if it doesn't exist (for graphs)
        create_system_table_query = """
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'RAM usage percentage',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Total RAM in MB',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Total bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_system_table_query)
        except Exception as table_error:
            print(f"Warning: Could not create system_metrics table: {str(table_error)}")
        
        # Create temporary_metrics table if it doesn't exist (for stat cards)
        create_temp_table_query = """
            CREATE TABLE IF NOT EXISTS temporary_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'RAM usage percentage',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Total RAM in MB',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Total bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_temp_table_query)
        except Exception as table_error:
            print(f"Warning: Could not create temporary_metrics table: {str(table_error)}")
        
        query = """
            SELECT 
                cpu_usage,
                ram_usage,
                ram_used_mb,
                ram_total_mb,
                bandwidth_in_mb,
                bandwidth_out_mb,
                bandwidth_total_mb,
                created_at
            FROM system_metrics
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
            ORDER BY created_at DESC
            LIMIT %s
        """
        
        metrics = execute_query(query, (hours, limit))
        
        # Ensure metrics is a list
        if not isinstance(metrics, list):
            metrics = []
        
        # Convert datetime objects to ISO format strings for JSON serialization
        serialized_metrics = []
        for metric in metrics:
            try:
                metric_dict = dict(metric) if isinstance(metric, dict) else metric
                # Convert created_at datetime to ISO format string
                if 'created_at' in metric_dict and metric_dict['created_at']:
                    if isinstance(metric_dict['created_at'], datetime):
                        metric_dict['created_at'] = metric_dict['created_at'].isoformat()
                    elif hasattr(metric_dict['created_at'], 'isoformat'):
                        metric_dict['created_at'] = metric_dict['created_at'].isoformat()
                    elif isinstance(metric_dict['created_at'], str):
                        # Already a string, keep as is
                        pass
                    else:
                        # Try to convert to string
                        metric_dict['created_at'] = str(metric_dict['created_at'])
                # Ensure all numeric values are properly typed
                for key in ['cpu_usage', 'ram_usage', 'ram_used_mb', 'ram_total_mb', 
                           'bandwidth_in_mb', 'bandwidth_out_mb', 'bandwidth_total_mb']:
                    if key in metric_dict and metric_dict[key] is not None:
                        try:
                            metric_dict[key] = float(metric_dict[key])
                        except (ValueError, TypeError):
                            metric_dict[key] = 0.0
                serialized_metrics.append(metric_dict)
            except Exception as metric_error:
                # Skip invalid metrics entries
                print(f"Warning: Skipping invalid metric entry: {str(metric_error)}")
                continue
        
        # Reverse to show chronological order
        if serialized_metrics:
            serialized_metrics.reverse()
        
        return jsonify({
            "success": True,
            "metrics": serialized_metrics
        })
    except Exception as e:
        print(f"Error fetching metrics: {str(e)}")
        traceback.print_exc()
        # Return a more user-friendly error response
        error_message = str(e)
        if 'table' in error_message.lower() and ('doesn\'t exist' in error_message.lower() or 'not found' in error_message.lower()):
            return jsonify({
                "success": True,
                "metrics": [],
                "message": "Metrics table not initialized. No metrics data available."
            })
        return jsonify({
            "success": False,
            "error": "Failed to fetch metrics. Please check server logs for details.",
            "details": error_message if DEBUG_MODE else None
        }), 500

@app.route("/api/admin/metrics/current", methods=["GET"])
@require_admin_auth
def get_current_metrics():
    """Get current system metrics from temporary_metrics table (for stat cards auto-refresh)"""
    try:
        # Create temporary_metrics table if it doesn't exist
        create_temp_table_query = """
            CREATE TABLE IF NOT EXISTS temporary_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpu_usage DECIMAL(5, 2) NOT NULL COMMENT 'CPU usage percentage',
                ram_usage DECIMAL(5, 2) NOT NULL COMMENT 'RAM usage percentage',
                ram_used_mb DECIMAL(10, 2) NOT NULL COMMENT 'RAM used in MB',
                ram_total_mb DECIMAL(10, 2) NOT NULL COMMENT 'Total RAM in MB',
                bandwidth_in_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth in (MB)',
                bandwidth_out_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Bandwidth out (MB)',
                bandwidth_total_mb DECIMAL(10, 2) DEFAULT 0 COMMENT 'Total bandwidth (MB)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at),
                INDEX idx_created_at_desc (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        try:
            execute_update(create_temp_table_query)
        except Exception as table_error:
            print(f"Warning: Could not create temporary_metrics table: {str(table_error)}")
        
        # Get the latest metrics from temporary_metrics table
        query = """
            SELECT 
                cpu_usage,
                ram_usage,
                ram_used_mb,
                ram_total_mb,
                bandwidth_in_mb,
                bandwidth_out_mb,
                bandwidth_total_mb,
                created_at
            FROM temporary_metrics
            ORDER BY created_at DESC
            LIMIT 1
        """
        
        metrics_result = execute_query(query)
        
        if metrics_result and len(metrics_result) > 0:
            # Return the latest metrics from temporary_metrics
            metric = metrics_result[0]
            return jsonify({
                "success": True,
                "metrics": {
                    "cpu_usage": float(metric.get('cpu_usage', 0)),
                    "ram_usage": float(metric.get('ram_usage', 0)),
                    "ram_used_mb": float(metric.get('ram_used_mb', 0)),
                    "ram_total_mb": float(metric.get('ram_total_mb', 0)),
                    "bandwidth_in_mb": float(metric.get('bandwidth_in_mb', 0)),
                    "bandwidth_out_mb": float(metric.get('bandwidth_out_mb', 0)),
                    "bandwidth_total_mb": float(metric.get('bandwidth_total_mb', 0)),
                    "created_at": metric.get('created_at').isoformat() if metric.get('created_at') else None
                }
            })
        else:
            # Fallback: Get current metrics without storing (if no data in temporary_metrics)
            try:
                # Get CPU usage for this application process only
                if psutil:
                    current_process = psutil.Process(os.getpid())
                    cpu_percent = current_process.cpu_percent(interval=0.1)
                    if cpu_percent is None:
                        cpu_percent = 0.0
                    # Normalize to percentage
                    num_cores = psutil.cpu_count() or 1
                    cpu_percent = min(100.0, (cpu_percent / num_cores) * 100) if num_cores > 0 else cpu_percent
                else:
                    cpu_percent = 0.0
                
                # Get RAM usage for this application process only
                if psutil:
                    current_process = psutil.Process(os.getpid())
                    process_memory = current_process.memory_info()
                    ram_used_mb = process_memory.rss / (1024 * 1024)
                    system_memory = psutil.virtual_memory()
                    ram_total_mb = system_memory.total / (1024 * 1024)
                    ram_percent = (ram_used_mb / ram_total_mb * 100) if ram_total_mb > 0 else 0.0
                else:
                    ram_percent = 0.0
                    ram_used_mb = 0.0
                    ram_total_mb = 0.0
                
                # Get bandwidth for this application
                with _bandwidth_lock:
                    bandwidth_in = _app_bandwidth_in
                    bandwidth_out = _app_bandwidth_out
                    bandwidth_total = bandwidth_in + bandwidth_out
                
                return jsonify({
                    "success": True,
                    "metrics": {
                        "cpu_usage": cpu_percent,
                        "ram_usage": ram_percent,
                        "ram_used_mb": round(ram_used_mb, 2),
                        "ram_total_mb": round(ram_total_mb, 2),
                        "bandwidth_in_mb": round(bandwidth_in, 2),
                        "bandwidth_out_mb": round(bandwidth_out, 2),
                        "bandwidth_total_mb": round(bandwidth_total, 2),
                        "created_at": None
                    },
                    "message": "No metrics in temporary_metrics table yet. Using live system data."
                })
            except Exception as fallback_error:
                print(f"Error in fallback metrics calculation: {str(fallback_error)}")
                return jsonify({
                    "success": False,
                    "error": "No metrics available and cannot calculate live metrics",
                    "details": str(fallback_error)
                }), 500
    except Exception as e:
        print(f"Error getting current metrics: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/admin/stats/dashboard", methods=["GET"])
@require_admin_auth
def get_dashboard_stats():
    """Get dashboard statistics (admin endpoint)"""
    try:
        def get_count(query):
            result = execute_query(query)
            return result[0]['count'] if result else 0
        
        # Count properties from both tables
        total_properties = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties UNION ALL SELECT id FROM plot_properties) as combined")
        active_properties = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties WHERE is_active = 1 UNION ALL SELECT id FROM plot_properties WHERE is_active = 1) as combined")
        featured_properties = get_count("SELECT COUNT(*) as count FROM (SELECT id FROM residential_properties WHERE is_featured = 1 UNION ALL SELECT id FROM plot_properties WHERE is_featured = 1) as combined")
        total_partners = get_count("SELECT COUNT(*) as count FROM partners")
        active_partners = get_count("SELECT COUNT(*) as count FROM partners WHERE is_active = 1")
        total_testimonials = get_count("SELECT COUNT(*) as count FROM testimonials")
        approved_testimonials = get_count("SELECT COUNT(*) as count FROM testimonials WHERE is_approved = 1")
        new_inquiries = get_count("SELECT COUNT(*) as count FROM contact_inquiries WHERE status = 'new'")
        total_inquiries = get_count("SELECT COUNT(*) as count FROM contact_inquiries")
        total_logs = get_count("SELECT COUNT(*) as count FROM logs")
        
        # Get type stats from both tables
        type_stats_res = execute_query("SELECT type, COUNT(*) as count FROM residential_properties GROUP BY type")
        type_stats_plot = execute_query("SELECT 'plot' as type, COUNT(*) as count FROM plot_properties")
        properties_by_type = {}
        if type_stats_res:
            for row in type_stats_res:
                properties_by_type[row['type']] = row['count']
        if type_stats_plot and type_stats_plot[0]['count'] > 0:
            properties_by_type['plot'] = properties_by_type.get('plot', 0) + type_stats_plot[0]['count']
        
        # Get status stats from both tables
        status_stats = execute_query("SELECT status, COUNT(*) as count FROM (SELECT status FROM residential_properties UNION ALL SELECT status FROM plot_properties) as combined GROUP BY status")
        properties_by_status = {row['status']: row['count'] for row in status_stats} if status_stats else {}
        
        result = DashboardStatsSchema(
            total_properties=total_properties,
            active_properties=active_properties,
            featured_properties=featured_properties,
            total_partners=total_partners,
            active_partners=active_partners,
            total_testimonials=total_testimonials,
            approved_testimonials=approved_testimonials,
            new_inquiries=new_inquiries,
            total_inquiries=total_inquiries,
            total_logs=total_logs,
            properties_by_type=properties_by_type,
            properties_by_status=properties_by_status
        )
        return jsonify(result.dict())
    except Exception as e:
        print(f"Error fetching dashboard stats: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error fetching dashboard stats: {str(e)}")


# ============================================
# ROUTES - STATIC FILES
# ============================================

@app.route("/css/<path:file_path>", methods=["GET"])
def serve_css(file_path: str):
    """Serve CSS files"""
    try:
        if ".." in file_path or file_path.startswith("/"):
            abort_with_message(400, "Invalid file path")
        
        css_path = FRONTEND_DIR / "css" / file_path
        try:
            css_path = css_path.resolve()
            css_dir = (FRONTEND_DIR / "css").resolve()
            if not str(css_path).startswith(str(css_dir)):
                abort_with_message(403, "Access denied")
        except Exception as e:
            print(f"Error resolving CSS path: {str(e)}")
            abort_with_message(400, "Invalid file path")
        
        if css_path.exists() and css_path.is_file():
            return send_file(str(css_path), mimetype="text/css")
        abort_with_message(404, "CSS file not found")
    except Exception as e:
        print(f"Error serving CSS: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error serving CSS: {str(e)}")


@app.route("/js/<path:file_path>", methods=["GET"])
def serve_js(file_path: str):
    """Serve JavaScript files"""
    try:
        if ".." in file_path or file_path.startswith("/"):
            abort_with_message(400, "Invalid file path")
        
        js_path = FRONTEND_DIR / "js" / file_path
        try:
            js_path = js_path.resolve()
            js_dir = (FRONTEND_DIR / "js").resolve()
            if not str(js_path).startswith(str(js_dir)):
                abort_with_message(403, "Access denied")
        except Exception as e:
            print(f"Error resolving JS path: {str(e)}")
            abort_with_message(400, "Invalid file path")
        
        if js_path.exists() and js_path.is_file():
            response = send_file(str(js_path), mimetype="application/javascript")
            # Check if there's a version query parameter - if so, don't cache
            if request.args.get('v'):
                # Version parameter present - don't cache, always serve fresh
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
            else:
                # No version parameter - allow caching
                response.headers['Cache-Control'] = 'public, max-age=3600, must-revalidate'
            return response
        abort_with_message(404, "JS file not found")
    except Exception as e:
        print(f"Error serving JS: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error serving JS: {str(e)}")


@app.route("/frontend/assets/css/<path:file_path>", methods=["GET"])
def serve_frontend_assets_css(file_path: str):
    """Serve CSS files from /frontend/assets/css/ for backward compatibility"""
    try:
        if ".." in file_path or file_path.startswith("/"):
            abort_with_message(400, "Invalid file path")
        
        css_path = FRONTEND_DIR / "css" / file_path
        try:
            css_path = css_path.resolve()
            css_dir = (FRONTEND_DIR / "css").resolve()
            if not str(css_path).startswith(str(css_dir)):
                abort_with_message(403, "Access denied")
        except Exception as e:
            print(f"Error resolving CSS path: {str(e)}")
            abort_with_message(400, "Invalid file path")
        
        if css_path.exists() and css_path.is_file():
            return send_file(str(css_path), mimetype="text/css")
        abort_with_message(404, "CSS file not found")
    except Exception as e:
        print(f"Error serving frontend assets CSS: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error serving CSS: {str(e)}")


@app.route("/frontend/assets/js/<path:file_path>", methods=["GET"])
def serve_frontend_assets_js(file_path: str):
    """Serve JavaScript files from /frontend/assets/js/ for backward compatibility"""
    try:
        if ".." in file_path or file_path.startswith("/"):
            abort_with_message(400, "Invalid file path")
        
        js_path = FRONTEND_DIR / "js" / file_path
        try:
            js_path = js_path.resolve()
            js_dir = (FRONTEND_DIR / "js").resolve()
            if not str(js_path).startswith(str(js_dir)):
                abort_with_message(403, "Access denied")
        except Exception as e:
            print(f"Error resolving JS path: {str(e)}")
            abort_with_message(400, "Invalid file path")
        
        if js_path.exists() and js_path.is_file():
            return send_file(str(js_path), mimetype="application/javascript")
        abort_with_message(404, "JS file not found")
    except Exception as e:
        print(f"Error serving frontend assets JS: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error serving JS: {str(e)}")


@app.route("/images/<path:file_path>", methods=["GET"])
def serve_image(file_path: str):
    """Serve image files explicitly - handles subdirectories like properties/"""
    try:
        if ".." in file_path or file_path.startswith("/"):
            abort_with_message(400, "Invalid file path")
        
        # Build the image path
        image_path = FRONTEND_DIR / "images" / file_path
        
        # Ensure the images directory exists
        images_dir = FRONTEND_DIR / "images"
        if not images_dir.exists():
            print(f"Images directory does not exist: {images_dir}")
            abort_with_message(404, "Image not found")
        
        # Resolve paths for security check (case-insensitive on Windows)
        try:
            image_path_resolved = image_path.resolve()
            images_dir_resolved = images_dir.resolve()
            
            # Normalize paths for comparison (handle Windows case-insensitivity)
            image_path_str = str(image_path_resolved).lower()
            images_dir_str = str(images_dir_resolved).lower()
            
            if not image_path_str.startswith(images_dir_str):
                abort_with_message(403, "Access denied")
        except Exception as e:
            print(f"Error resolving image path: {str(e)}")
            abort_with_message(400, "Invalid file path")
        
        # Check if file exists and is a file (not a directory)
        if not image_path.exists():
            print(f"Image file does not exist: {image_path}")
            abort_with_message(404, "Image not found")
        
        if not image_path.is_file():
            print(f"Image path is not a file: {image_path}")
            abort_with_message(404, "Image not found")
        
        # Serve the file
        return send_file(str(image_path))
    except Exception as e:
        # Check if this is a Flask/Werkzeug HTTPException (from abort_with_message)
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            # Re-raise HTTP exceptions (400, 403, 404) to let Flask handle them
            raise
        print(f"Error serving image: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error serving image: {str(e)}")


@app.route("/frontend/assets/images/<path:file_path>", methods=["GET"])
def serve_frontend_assets_image(file_path: str):
    """Serve image files from /frontend/assets/images/ for backward compatibility"""
    try:
        if ".." in file_path or file_path.startswith("/"):
            abort_with_message(400, "Invalid file path")
        
        image_path = FRONTEND_DIR / "images" / file_path
        try:
            image_path = image_path.resolve()
            images_dir = (FRONTEND_DIR / "images").resolve()
            if not str(image_path).startswith(str(images_dir)):
                abort_with_message(403, "Access denied")
        except Exception as e:
            print(f"Error resolving image path: {str(e)}")
            abort_with_message(400, "Invalid file path")
        
        if image_path.exists() and image_path.is_file():
            return send_file(str(image_path))
        abort_with_message(404, "Image not found")
    except Exception as e:
        print(f"Error serving frontend assets image: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error serving image: {str(e)}")


# ============================================
# ROUTES - FRONTEND HTML PAGES
# ============================================

@app.route("/frontend/pages/<page_name>.html", methods=["GET"])
def serve_frontend_page(page_name: str):
    """Serve frontend HTML pages from /frontend/pages/ path (backward compatibility)"""
    try:
        if not FRONTEND_DIR or not FRONTEND_DIR.exists():
            abort_with_message(500, "Frontend directory not configured")
        
        if ".." in page_name or "/" in page_name:
            abort_with_message(400, "Invalid page name")
        
        page_path = FRONTEND_DIR / f"{page_name}.html"
        if page_path.exists() and page_path.is_file():
            return send_file(str(page_path))
        abort_with_message(404, "Page not found")
    except Exception as e:
        print(f"Error serving frontend page: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error serving page: {str(e)}")


@app.route("/properties", methods=["GET"])
def properties_page():
    """Serve the properties page"""
    try:
        if not FRONTEND_DIR or not FRONTEND_DIR.exists():
            abort_with_message(500, "Frontend directory not configured")
        
        properties_path = FRONTEND_DIR / "properties.html"
        if properties_path.exists() and properties_path.is_file():
            return send_file(str(properties_path))
        abort_with_message(404, "Page not found")
    except Exception as e:
        print(f"Error serving properties page: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error serving page: {str(e)}")


@app.route("/properties.html", methods=["GET"])
def properties_page_html():
    """Serve the properties page (with .html extension)"""
    properties_path = FRONTEND_DIR / "properties.html"
    if properties_path.exists():
        return send_file(str(properties_path))
    abort_with_message(404, "Page not found")


@app.route("/property-details", methods=["GET"])
def property_details_page():
    """Serve the property details page"""
    details_path = FRONTEND_DIR / "property-details.html"
    if details_path.exists():
        return send_file(str(details_path))
    abort_with_message(404, "Page not found")


@app.route("/property-details.html", methods=["GET"])
def property_details_page_html():
    """Serve the property details page (with .html extension)"""
    details_path = FRONTEND_DIR / "property-details.html"
    if details_path.exists():
        return send_file(str(details_path))
    abort_with_message(404, "Page not found")


@app.route("/blogs", methods=["GET"])
def blogs_page():
    """Serve the blogs page"""
    blogs_path = FRONTEND_DIR / "blogs.html"
    if blogs_path.exists():
        return send_file(str(blogs_path))
    abort_with_message(404, "Page not found")


@app.route("/blogs.html", methods=["GET"])
def blogs_page_html():
    """Serve the blogs page (with .html extension)"""
    blogs_path = FRONTEND_DIR / "blogs.html"
    if blogs_path.exists():
        return send_file(str(blogs_path))
    abort_with_message(404, "Page not found")


@app.route("/blog-details", methods=["GET"])
def blog_details_page():
    """Serve the blog details page"""
    blog_details_path = FRONTEND_DIR / "blog-details.html"
    if blog_details_path.exists():
        return send_file(str(blog_details_path))
    abort_with_message(404, "Page not found")


@app.route("/blog-details.html", methods=["GET"])
def blog_details_page_html():
    """Serve the blog details page (with .html extension)"""
    blog_details_path = FRONTEND_DIR / "blog-details.html"
    if blog_details_path.exists():
        return send_file(str(blog_details_path))
    abort_with_message(404, "Page not found")


@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    """Serve the dashboard page"""
    dashboard_path = FRONTEND_DIR / "dashboard.html"
    if dashboard_path.exists():
        # Read the HTML file and inject cache-busting timestamp
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Replace ANY version number with current timestamp for cache busting
        import time
        import re
        cache_buster = str(int(time.time()))
        # Match dashboard.js?v= followed by any characters (version number)
        html_content = re.sub(
            r'dashboard\.js\?v=[^"\']+',
            f'dashboard.js?v={cache_buster}',
            html_content
        )
        
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        # Add cache-control headers to prevent aggressive caching of HTML
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    abort_with_message(404, "Page not found")


@app.route("/dashboard.html", methods=["GET"])
def dashboard_page_html():
    """Serve the dashboard page (with .html extension)"""
    dashboard_path = FRONTEND_DIR / "dashboard.html"
    if dashboard_path.exists():
        # Read the HTML file and inject cache-busting timestamp
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Replace ANY version number with current timestamp for cache busting
        import time
        import re
        cache_buster = str(int(time.time()))
        # Match dashboard.js?v= followed by any characters (version number)
        html_content = re.sub(
            r'dashboard\.js\?v=[^"\']+',
            f'dashboard.js?v={cache_buster}',
            html_content
        )
        
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        # Add cache-control headers to prevent aggressive caching of HTML
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    abort_with_message(404, "Page not found")


@app.route("/database", methods=["GET"])
def database_page():
    """Serve the database export page"""
    database_path = FRONTEND_DIR / "database.html"
    if database_path.exists():
        return send_file(str(database_path))
    abort_with_message(404, "Page not found")


@app.route("/database.html", methods=["GET"])
def database_page_html():
    """Serve the database export page (with .html extension)"""
    database_path = FRONTEND_DIR / "database.html"
    if database_path.exists():
        return send_file(str(database_path))
    abort_with_message(404, "Page not found")


@app.route("/terms-and-conditions", methods=["GET"])
def terms_and_conditions_page():
    """Serve the terms and conditions page"""
    terms_path = FRONTEND_DIR / "terms-and-conditions.html"
    if terms_path.exists():
        return send_file(str(terms_path))
    abort_with_message(404, "Page not found")


@app.route("/terms-and-conditions.html", methods=["GET"])
def terms_and_conditions_page_html():
    """Serve the terms and conditions page (with .html extension)"""
    terms_path = FRONTEND_DIR / "terms-and-conditions.html"
    if terms_path.exists():
        return send_file(str(terms_path))
    abort_with_message(404, "Page not found")


@app.route("/privacy-policy", methods=["GET"])
def privacy_policy_page():
    """Serve the privacy policy page"""
    privacy_path = FRONTEND_DIR / "privacy-policy.html"
    if privacy_path.exists():
        return send_file(str(privacy_path))
    abort_with_message(404, "Page not found")


@app.route("/privacy-policy.html", methods=["GET"])
def privacy_policy_page_html():
    """Serve the privacy policy page (with .html extension)"""
    privacy_path = FRONTEND_DIR / "privacy-policy.html"
    if privacy_path.exists():
        return send_file(str(privacy_path))
    abort_with_message(404, "Page not found")


@app.route("/nri-property-investment", methods=["GET"])
def nri_property_investment_page():
    """Serve the NRI property investment page"""
    nri_path = FRONTEND_DIR / "nri-property-investment.html"
    if nri_path.exists():
        return send_file(str(nri_path))
    abort_with_message(404, "Page not found")


@app.route("/nri-property-investment.html", methods=["GET"])
def nri_property_investment_page_html():
    """Serve the NRI property investment page (with .html extension)"""
    nri_path = FRONTEND_DIR / "nri-property-investment.html"
    if nri_path.exists():
        return send_file(str(nri_path))
    abort_with_message(404, "Page not found")


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    """Serve favicon.ico - returns the logo PNG or 204 No Content"""
    try:
        favicon_path = FRONTEND_DIR / "images" / "TirumakudaluProperties_Logo-2048x1858.png"
        if favicon_path.exists() and favicon_path.is_file():
            return send_file(str(favicon_path), mimetype="image/png")
        return make_response("", 204)
    except Exception as e:
        print(f"Error serving favicon: {str(e)}")
        return make_response("", 204)


# ============================================
# ROUTES - DATABASE EXPORT/IMPORT
# ============================================

@app.route("/api/admin/export/database", methods=["GET"])
@require_admin_auth
def export_database_to_csv():
    """Export all database data to CSV file"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        tables = [
            ("residential_properties", [
                "id", "city", "locality", "property_name", "unit_type", "bedrooms", 
                "buildup_area", "carpet_area", "price", "price_text", "price_negotiable", 
                "price_includes_registration", "type", "status", "property_status", 
                "description", "is_featured", "is_active", "created_at", "updated_at"
            ]),
            ("plot_properties", [
                "id", "city", "locality", "project_name", "plot_area", "plot_length", 
                "plot_breadth", "price", "price_text", "price_negotiable", 
                "price_includes_registration", "status", "property_status", 
                "description", "is_featured", "is_active", "created_at", "updated_at"
            ]),
            ("residential_property_images", [
                "id", "property_id", "image_url", "image_order", 
                "is_primary", "created_at"
            ]),
            ("plot_property_images", [
                "id", "property_id", "image_url", "image_order", 
                "is_primary", "created_at"
            ]),
            ("residential_property_features", [
                "id", "property_id", "feature_name", "created_at"
            ]),
            ("plot_property_features", [
                "id", "property_id", "feature_name", "created_at"
            ]),
            ("partners", [
                "id", "name", "logo_url", "website_url", "is_active", 
                "display_order", "created_at", "updated_at"
            ]),
            ("testimonials", [
                "id", "client_name", "client_email", "client_phone", 
                "service_type", "rating", "message", "is_approved", 
                "is_featured", "created_at", "updated_at"
            ]),
            ("contact_inquiries", [
                "id", "name", "email", "subject", "message", "phone", 
                "property_id", "status", "created_at", "updated_at"
            ]),
            ("users", [
                "id", "email", "full_name", "role", "is_active", 
                "last_login", "created_at", "updated_at"
            ])
        ]
        
        for table_name, columns in tables:
            writer.writerow([f"=== {table_name.upper()} TABLE ==="])
            writer.writerow(columns)
            
            try:
                query = f"SELECT {', '.join(columns)} FROM {table_name} ORDER BY id"
                rows = execute_query(query)
                
                for row in rows:
                    csv_row = [str(row.get(col, '')) if row.get(col) is not None else '' for col in columns]
                    writer.writerow(csv_row)
                
                writer.writerow([])
            except Exception as e:
                writer.writerow([f"Error fetching data: {str(e)}"])
                writer.writerow([])
        
        csv_content = output.getvalue()
        output.close()
        
        csv_bytes = io.BytesIO(csv_content.encode('utf-8-sig'))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"database_export_{timestamp}.csv"
        
        response = make_response(csv_bytes.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
        
    except Exception as e:
        print(f"Error exporting database: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error exporting database: {str(e)}")


@app.route("/api/admin/export/table/<table_name>", methods=["GET"])
@require_admin_auth
def export_table_to_csv(table_name: str):
    """Export a specific table to CSV file"""
    try:
        table_configs = {
            "residential_properties": {
                "columns": [
                    "id", "city", "locality", "property_name", "unit_type", "bedrooms", 
                    "buildup_area", "carpet_area", "price", "price_text", "price_negotiable", 
                    "price_includes_registration", "type", "status", "property_status", 
                    "description", "is_featured", "is_active", "created_at", "updated_at"
                ],
                "display_name": "Residential_Properties"
            },
            "plot_properties": {
                "columns": [
                    "id", "city", "locality", "project_name", "plot_area", "plot_length", 
                    "plot_breadth", "price", "price_text", "price_negotiable", 
                    "price_includes_registration", "status", "property_status", 
                    "description", "is_featured", "is_active", "created_at", "updated_at"
                ],
                "display_name": "Plot_Properties"
            },
            "properties": {
                "columns": [
                    "id", "city", "locality", "property_name", "unit_type", "bedrooms", 
                    "buildup_area", "carpet_area", "price", "price_text", "price_negotiable", 
                    "price_includes_registration", "type", "status", "property_status", 
                    "description", "is_featured", "is_active", "created_at", "updated_at",
                    "property_category"
                ],
                "display_name": "Properties",
                "query": """
                    SELECT 
                        id, city, locality, property_name, unit_type, bedrooms, 
                        buildup_area, carpet_area, price, price_text, price_negotiable, 
                        price_includes_registration, type, status, property_status, 
                        description, is_featured, is_active, created_at, updated_at,
                        'residential' as property_category
                    FROM residential_properties
                    UNION ALL
                    SELECT 
                        id, city, locality, project_name as property_name, NULL as unit_type, 0 as bedrooms, 
                        plot_area as buildup_area, NULL as carpet_area, price, price_text, price_negotiable, 
                        price_includes_registration, 'plot' as type, status, property_status, 
                        description, is_featured, is_active, created_at, updated_at,
                        'plot' as property_category
                    FROM plot_properties
                    ORDER BY created_at DESC
                """
            },
            "testimonials": {
                "columns": [
                    "id", "client_name", "client_email", "client_phone", 
                    "service_type", "rating", "message", "is_approved", 
                    "is_featured", "created_at", "updated_at"
                ],
                "display_name": "Testimonials"
            },
            "partners": {
                "columns": [
                    "id", "name", "logo_url", "website_url", "is_active", 
                    "display_order", "created_at", "updated_at"
                ],
                "display_name": "Partners"
            },
            "contact_inquiries": {
                "columns": [
                    "id", "name", "email", "subject", "message", "phone", 
                    "property_id", "status", "created_at", "updated_at"
                ],
                "display_name": "Schedule_Visit_Requests",
                "filter": "subject = 'Schedule Visit' AND status != 'closed'"
            },
            "visitor_info": {
                "columns": [
                    "id", "full_name", "email", "phone", "looking_for", "created_at"
                ],
                "display_name": "Website_Visitors"
            },
            "logs": {
                "columns": [
                    "id", "log_type", "action", "description", "user_email", 
                    "ip_address", "user_agent", "metadata", "created_at"
                ],
                "display_name": "Activity_Logs"
            }
        }
        
        if table_name not in table_configs:
            abort_with_message(400, f"Table '{table_name}' is not supported for export")
        
        config = table_configs[table_name]
        columns = config["columns"]
        display_name = config["display_name"]
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(columns)
        
        # Check if custom query is provided (for combined properties export)
        if "query" in config:
            query = config["query"]
        else:
            query = f"SELECT {', '.join(columns)} FROM {table_name}"
            if "filter" in config:
                query += f" WHERE {config['filter']}"
            query += " ORDER BY id"
        
        try:
            rows = execute_query(query)
            
            for row in rows:
                csv_row = [str(row.get(col, '')) if row.get(col) is not None else '' for col in columns]
                writer.writerow(csv_row)
        except Exception as e:
            abort_with_message(500, f"Error fetching data from {table_name}: {str(e)}")
        
        csv_content = output.getvalue()
        output.close()
        
        csv_bytes = io.BytesIO(csv_content.encode('utf-8-sig'))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{display_name}_{timestamp}.csv"
        
        response = make_response(csv_bytes.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
        
    except Exception as e:
        print(f"Error exporting table {table_name}: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error exporting table: {str(e)}")


@app.route("/api/admin/import/table/<table_name>", methods=["POST"])
@require_admin_auth
def import_table_from_csv(table_name: str):
    """Import data from CSV file into a specific table"""
    try:
        if 'file' not in request.files:
            abort_with_message(400, "No file provided")
        
        file = request.files['file']
        if file.filename == '':
            abort_with_message(400, "No file selected")
        
        table_configs = {
            "residential_properties": {
                "columns": [
                    "id", "city", "locality", "property_name", "unit_type", "bedrooms", 
                    "buildup_area", "carpet_area", "price", "price_text", "price_negotiable", 
                    "price_includes_registration", "type", "status", "property_status", 
                    "description", "is_featured", "is_active", "created_at", "updated_at"
                ],
                "display_name": "Residential_Properties",
                "required_columns": ["city", "locality", "property_name", "unit_type", "bedrooms", 
                                     "buildup_area", "carpet_area", "price", "type", "status"],
                "auto_columns": ["id", "created_at", "updated_at"],
                "table_name": "residential_properties"
            },
            "plot_properties": {
                "columns": [
                    "id", "city", "locality", "project_name", "plot_area", "plot_length", 
                    "plot_breadth", "price", "price_text", "price_negotiable", 
                    "price_includes_registration", "status", "property_status", 
                    "description", "is_featured", "is_active", "created_at", "updated_at"
                ],
                "display_name": "Plot_Properties",
                "required_columns": ["city", "locality", "project_name", "plot_area", "plot_length", 
                                    "plot_breadth", "price", "status"],
                "auto_columns": ["id", "created_at", "updated_at"],
                "table_name": "plot_properties"
            },
            "properties": {
                "columns": [
                    "id", "city", "locality", "property_name", "unit_type", "bedrooms", 
                    "buildup_area", "carpet_area", "price", "price_text", "price_negotiable", 
                    "price_includes_registration", "type", "status", "property_status", 
                    "description", "is_featured", "is_active", "created_at", "updated_at",
                    "property_category"
                ],
                "display_name": "Properties",
                "required_columns": ["city", "locality", "property_name", "price", "status"],
                "auto_columns": ["id", "created_at", "updated_at"],
                "table_name": "properties"  # Will be determined by property_category
            },
            "testimonials": {
                "columns": [
                    "id", "client_name", "client_email", "client_phone", 
                    "service_type", "rating", "message", "is_approved", 
                    "is_featured", "created_at", "updated_at"
                ],
                "display_name": "Testimonials",
                "required_columns": ["client_name", "message"],
                "auto_columns": ["id", "created_at", "updated_at"]
            },
            "partners": {
                "columns": [
                    "id", "name", "logo_url", "website_url", "is_active", 
                    "display_order", "created_at", "updated_at"
                ],
                "display_name": "Partners",
                "required_columns": ["name"],
                "auto_columns": ["id", "created_at", "updated_at"]
            },
            "contact_inquiries": {
                "columns": [
                    "id", "name", "email", "subject", "message", "phone", 
                    "property_id", "status", "ip_address", "created_at", "updated_at"
                ],
                "display_name": "Schedule_Visit_Requests",
                "required_columns": ["name", "email", "message"],
                "auto_columns": ["id", "created_at", "updated_at"]
            },
            "visitor_info": {
                "columns": [
                    "id", "full_name", "email", "phone", "looking_for", "ip_address", "created_at"
                ],
                "display_name": "Website_Visitors",
                "required_columns": ["full_name", "email", "phone"],
                "auto_columns": ["id", "created_at"]
            },
            "logs": {
                "columns": [
                    "id", "log_type", "action", "description", "user_email", 
                    "ip_address", "user_agent", "metadata", "created_at"
                ],
                "display_name": "Activity_Logs",
                "required_columns": ["log_type", "action"],
                "auto_columns": ["id", "created_at"]
            }
        }
        
        if table_name not in table_configs:
            abort_with_message(400, f"Table '{table_name}' is not supported for import")
        
        config = table_configs[table_name]
        all_columns = config["columns"]
        required_columns = config["required_columns"]
        auto_columns = config.get("auto_columns", [])
        
        contents = file.read()
        csv_content = contents.decode('utf-8-sig')
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        csv_headers = csv_reader.fieldnames
        if not csv_headers:
            abort_with_message(400, "CSV file is empty or has no headers")
        
        # For properties import, check required columns based on property_category if present
        if table_name == "properties" and "property_category" in csv_headers:
            # Read first row to determine category
            first_row = next(csv_reader, None)
            if first_row:
                property_category = first_row.get("property_category", "").strip().lower()
                if property_category == "plot":
                    required_columns = ["city", "locality", "project_name", "plot_area", "plot_length", 
                                      "plot_breadth", "price", "status"]
                else:
                    required_columns = ["city", "locality", "property_name", "unit_type", "bedrooms", 
                                     "buildup_area", "carpet_area", "price", "type", "status"]
                # Reset reader to start
                csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        missing_required = [col for col in required_columns if col not in csv_headers]
        if missing_required:
            abort_with_message(400, f"Missing required columns: {', '.join(missing_required)}")
        
        # Determine target table
        target_table = config.get("table_name", table_name)
        
        rows_inserted = 0
        errors = []
        
        with get_db_cursor() as cursor:
            for row_num, row in enumerate(csv_reader, start=2):
                try:
                    # For properties import, determine which table to use based on property_category
                    if table_name == "properties" and "property_category" in csv_headers:
                        property_category = row.get("property_category", "").strip().lower()
                        if property_category == "plot":
                            target_table = "plot_properties"
                        else:
                            target_table = "residential_properties"
                    
                    # Get valid columns for target table
                    if target_table == "plot_properties":
                        valid_cols = ["id", "city", "locality", "project_name", "plot_area", "plot_length", 
                                     "plot_breadth", "price", "price_text", "price_negotiable", 
                                     "price_includes_registration", "status", "property_status", 
                                     "description", "is_featured", "is_active", "created_at", "updated_at"]
                        # Map property_name to project_name if needed
                        if "property_name" in csv_headers and "project_name" not in csv_headers:
                            row["project_name"] = row.get("property_name", "")
                        # Map buildup_area to plot_area if needed (from combined export)
                        if "buildup_area" in csv_headers and "plot_area" not in csv_headers:
                            row["plot_area"] = row.get("buildup_area", "")
                    elif target_table == "residential_properties":
                        valid_cols = ["id", "city", "locality", "property_name", "unit_type", "bedrooms", 
                                     "buildup_area", "carpet_area", "price", "price_text", "price_negotiable", 
                                     "price_includes_registration", "type", "status", "property_status", 
                                     "description", "is_featured", "is_active", "created_at", "updated_at"]
                        # Map project_name to property_name if needed
                        if "project_name" in csv_headers and "property_name" not in csv_headers:
                            row["property_name"] = row.get("project_name", "")
                    else:
                        valid_cols = all_columns
                    
                    insert_columns = [col for col in csv_headers if col in valid_cols and col not in auto_columns and col != "property_category"]
                    
                    placeholders = ', '.join(['%s'] * len(insert_columns))
                    insert_query = f"INSERT INTO {target_table} ({', '.join(insert_columns)}) VALUES ({placeholders})"
                    
                    values = []
                    for col in insert_columns:
                        # Handle column name mapping for plot properties
                        source_col = col
                        if target_table == "plot_properties" and col == "plot_area" and "buildup_area" in csv_headers and "plot_area" not in csv_headers:
                            source_col = "buildup_area"
                        
                        value = row.get(source_col, row.get(col, '')).strip() if source_col in row or col in row else ''
                        
                        if not value and col not in required_columns:
                            value = None
                        
                        # Handle numeric conversions
                        if col in ['bedrooms', 'plot_area', 'plot_length', 'plot_breadth', 'buildup_area', 'carpet_area', 
                                  'rating', 'property_id', 'display_order', 'is_active', 'is_featured', 'is_approved',
                                  'price_negotiable', 'price_includes_registration']:
                            if value:
                                try:
                                    if col in ['bedrooms', 'plot_area', 'plot_length', 'plot_breadth', 'rating', 'property_id', 'display_order']:
                                        value = int(value)
                                    elif col in ['buildup_area', 'carpet_area']:
                                        value = float(value)
                                    elif col in ['is_active', 'is_featured', 'is_approved', 'price_negotiable', 'price_includes_registration']:
                                        value = 1 if str(value).lower() in ['1', 'true', 'yes', 'y'] else 0
                                except ValueError:
                                    value = None if col not in required_columns else 0
                            else:
                                value = None if col not in required_columns else 0
                        
                        if col in ['price']:
                            if value:
                                try:
                                    value = float(value)
                                except ValueError:
                                    value = None
                            else:
                                value = None
                        
                        values.append(value)
                    
                    cursor.execute(insert_query, tuple(values))
                    rows_inserted += 1
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                    continue
        
        result = {
            "message": f"Import completed",
            "rows_inserted": rows_inserted,
            "total_rows": row_num - 1 if 'row_num' in locals() else 0
        }
        
        if errors:
            result["errors"] = errors[:10]
            result["error_count"] = len(errors)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error importing table {table_name}: {str(e)}")
        traceback.print_exc()
        abort_with_message(500, f"Error importing table: {str(e)}")


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 errors"""
    return jsonify({"error": "Unauthorized", "success": False}), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return jsonify({"error": "Forbidden", "success": False}), 403


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    if request.path.startswith(("/css/", "/js/", "/images/", "/frontend/assets/")):
        return make_response("Static file not found", 404)
    # Try to get error message from response data if available
    error_msg = "Not found"
    if hasattr(error, 'response') and hasattr(error.response, 'data'):
        try:
            error_data = json.loads(error.response.data)
            if isinstance(error_data, dict) and 'error' in error_data:
                error_msg = error_data['error']
        except:
            pass
    return jsonify({"error": error_msg, "success": False}), 404


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    error_msg = "Bad request"
    if hasattr(error, 'response') and hasattr(error.response, 'data'):
        try:
            error_data = json.loads(error.response.data)
            if isinstance(error_data, dict) and 'error' in error_data:
                error_msg = error_data['error']
        except:
            pass
    return jsonify({"error": error_msg, "success": False}), 400


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    error_msg = "Internal server error"
    if hasattr(error, 'response') and hasattr(error.response, 'data'):
        try:
            error_data = json.loads(error.response.data)
            if isinstance(error_data, dict) and 'error' in error_data:
                error_msg = error_data['error']
        except:
            pass
    return jsonify({"error": error_msg, "success": False}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle general exceptions"""
    import traceback
    error_trace = traceback.format_exc()
    print(f"Unhandled exception: {str(e)}")
    print(f"Request path: {request.path}")
    print(f"Traceback:\n{error_trace}")
    
    if request.path.startswith(("/css/", "/js/", "/images/", "/frontend/assets/")):
        return make_response("Static file not found", 404)
    
    # Don't expose internal error details in production
    error_detail = str(e) if DEBUG_MODE else "An internal error occurred. Please contact support."
    return jsonify({"error": "Internal server error", "detail": error_detail, "success": False}), 500


# ============================================
# APPLICATION ENTRY POINT
# ============================================

# For WSGI servers (Passenger, mod_wsgi, etc.)
# They will load: from app import application
application = app

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host="0.0.0.0", port=5000)