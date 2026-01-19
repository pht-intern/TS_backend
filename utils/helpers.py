"""
Helper functions for request handling, pagination, image processing, etc.
"""
import os
import uuid
import base64
import traceback
from typing import List, Optional
from pathlib import Path
from flask import request, jsonify, abort, make_response
from schemas import PaginationParams
from database import test_connection, execute_query


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


def save_base64_image(base64_string: str, images_dir: Path = None) -> str:
    """Convert base64 image to file and save it. Returns the relative URL path."""
    if not base64_string.startswith('data:image/'):
        return base64_string
    
    try:
        # Use config if images_dir not provided
        if images_dir is None:
            from config import IMAGES_DIR
            images_dir = IMAGES_DIR
        
        header, data = base64_string.split(',', 1)
        format_part = header.split(';')[0]
        image_format = format_part.split('/')[-1]
        
        image_data = base64.b64decode(data)
        
        # Handle both old structure (images_dir/images/properties) and new (images_dir/properties)
        # Check if images_dir already contains "images" subdirectory
        if images_dir.name == "images":
            property_images_dir = images_dir / "properties"
        else:
            # Old structure: images_dir is FRONTEND_DIR, so we need images_dir/images/properties
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


def save_partner_logo(logo_url: Optional[str], images_dir: Path = None) -> Optional[str]:
    """Process partner logo - convert base64 to file if needed."""
    if not logo_url:
        return None
    
    if not logo_url.startswith('data:image/'):
        return logo_url
    
    try:
        # Use config if images_dir not provided
        if images_dir is None:
            from config import IMAGES_DIR
            images_dir = IMAGES_DIR
        
        header, data = logo_url.split(',', 1)
        format_part = header.split(';')[0]
        image_format = format_part.split('/')[-1]
        
        image_data = base64.b64decode(data)
        
        # Handle both old structure (images_dir/images/logos) and new (images_dir/logos)
        # Check if images_dir already contains "images" subdirectory
        if images_dir.name == "images":
            logos_dir = images_dir / "logos"
        else:
            # Old structure: images_dir is FRONTEND_DIR, so we need images_dir/images/logos
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


def process_image_urls(image_urls: List[str], images_dir: Path = None) -> List[str]:
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


def abort_with_message(status_code: int, message: str):
    """Helper function to abort with a custom error message"""
    response = make_response(jsonify({"error": message, "success": False}), status_code)
    abort(response)


def safe_int(value, default=0):
    """Safely convert a value to int, handling None, empty strings, and invalid values"""
    if value is None:
        return default
    if isinstance(value, str):
        value = value.strip()
        if value == '' or value.lower() == 'nan' or value.lower() == 'none':
            return default
    try:
        return int(float(value))  # Convert to float first to handle string numbers
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    """Safely convert a value to float, handling None, empty strings, and invalid values"""
    if value is None:
        return default
    if isinstance(value, str):
        value = value.strip()
        if value == '' or value.lower() == 'nan' or value.lower() == 'none':
            return default
        # Try to extract numeric value from strings like "Rs. 10", "10 Cr", etc.
        # Remove common currency symbols and text
        import re
        # Remove currency symbols and common text
        cleaned = re.sub(r'[Rs\.₹,\s]', '', value, flags=re.IGNORECASE)
        # Try to extract just the number part
        number_match = re.search(r'[\d.]+', cleaned)
        if number_match:
            value = number_match.group(0)
    try:
        result = float(value)
        # Check for NaN or infinity
        if not (result == result):  # NaN check
            return default
        if result == float('inf') or result == float('-inf'):
            return default
        return result
    except (ValueError, TypeError):
        return default


def require_admin_auth(f):
    """
    Decorator to require admin authentication for protected routes.
    Verifies user exists in database and has admin role.
    """
    from functools import wraps
    
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
