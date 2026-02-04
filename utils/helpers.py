"""
Helper functions for request handling, auth, validation, and responses.
PRODUCTION-SAFE VERSION
"""

import os
import uuid
import base64
import traceback
from typing import List, Optional
from pathlib import Path

from flask import request, jsonify
from schemas import PaginationParams
from database import test_connection, execute_query


# ==========================================================
# CLIENT IP
# ==========================================================
def get_client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    return request.remote_addr


# ==========================================================
# PAGINATION
# ==========================================================
def get_pagination_params() -> PaginationParams:
    page = max(int(request.args.get("page", 1)), 1)
    limit = min(max(int(request.args.get("limit", 10)), 1), 100)
    return PaginationParams(page=page, limit=limit)


def calculate_pages(total: int, limit: int) -> int:
    return (total + limit - 1) // limit if total > 0 else 0


# ==========================================================
# IMAGE HANDLING
# ==========================================================
def save_base64_image(base64_string: str, images_dir: Path = None) -> Optional[str]:
    if not base64_string or not base64_string.startswith("data:image/"):
        return base64_string

    try:
        if images_dir is None:
            from config import IMAGES_DIR
            images_dir = IMAGES_DIR

        # Split base64 string into header and data
        if "," not in base64_string:
            raise ValueError("Invalid base64 image format: missing comma separator")
        
        header, data = base64_string.split(",", 1)
        
        # Extract image format from header (e.g., "data:image/jpeg;base64" -> "jpeg")
        if "/" not in header or ";" not in header:
            raise ValueError(f"Invalid base64 image header format: {header[:50]}")
        
        format_part = header.split("/")[1].split(";")[0]
        image_format = format_part.lower()
        
        # Validate and normalize image format
        # Map common formats to file extensions - support all common image formats
        format_map = {
            'jpeg': 'jpg',  # Use .jpg extension for JPEG
            'jpg': 'jpg',
            'png': 'png',
            'gif': 'gif',
            'webp': 'webp',
            'svg+xml': 'svg',
            'svg': 'svg',
            'bmp': 'bmp',
            'ico': 'ico',
            'tiff': 'tiff',
            'tif': 'tiff',
            'heic': 'heic',
            'heif': 'heif',
            'avif': 'avif'
        }
        
        # If format not in map, try to use it directly (for unknown formats)
        if image_format not in format_map:
            # For unknown formats, try to use the format name directly
            # Remove any + characters and use as extension
            file_extension = image_format.replace('+', '').split(';')[0]
            print(f"Warning: Unknown image format '{image_format}', using extension '{file_extension}'")
        else:
            file_extension = format_map[image_format]
        
        # Decode base64 data
        try:
            image_data = base64.b64decode(data, validate=True)
        except Exception as decode_error:
            raise ValueError(f"Invalid base64 data: {str(decode_error)}")
        
        # Validate that we actually got image data
        if not image_data or len(image_data) == 0:
            raise ValueError("Decoded image data is empty")

        # Determine target directory
        if images_dir.name == "images":
            target_dir = images_dir / "properties"
        else:
            target_dir = images_dir / "images" / "properties"

        target_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename with proper extension
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = target_dir / filename

        # Write image file
        with open(file_path, "wb") as f:
            f.write(image_data)

        # Return the URL path (relative to web root)
        return f"/images/properties/{filename}"

    except Exception as e:
        print(f"Image save failed: {e}")
        import traceback
        traceback.print_exc()
        # Return None to indicate failure (caller should check for this)
        return None


def process_image_urls(image_urls: List[str], images_dir: Path = None) -> List[str]:
    return [
        save_base64_image(url, images_dir) if url and url.startswith("data:image/") else url
        for url in image_urls
    ]


def normalize_image_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None

    if url.startswith(("http://", "https://", "data:")):
        return url

    # If URL is already in /api/images/{id} format, return as is
    if url.startswith("/api/images/"):
        return url

    if "/public_html/" in url:
        url = "/" + url.split("/public_html/", 1)[1].lstrip("/")

    # Check if URL is a numeric ID (database-stored image)
    # Strip leading/trailing slashes and check if it's a pure number
    url_clean = url.lstrip('/').rstrip('/')
    
    # Check if it's a numeric ID (either just a number, or /images/{number})
    if url_clean.isdigit():
        # It's a numeric ID, convert to /api/images/{id}
        return f"/api/images/{url_clean}"
    
    # Check if it's /images/{number} format
    if url.startswith("/images/"):
        # Extract the part after /images/
        after_images = url[8:].lstrip('/')  # 8 = len("/images/")
        if after_images.isdigit():
            # It's /images/{number}, convert to /api/images/{number}
            return f"/api/images/{after_images}"
        # Otherwise, it's a file path, keep as is
        return url

    # For file paths, ensure they start with /images/
    return url if url.startswith("/images/") else f"/images/{url.lstrip('/')}"


def get_image_url_from_logo_url(logo_url: Optional[str]) -> Optional[str]:
    """
    Convert logo_url to image_url in /uploads/{filename} format.
    Extracts the filename from various URL formats and returns /uploads/{filename}.
    This is used for partners/testimonials where backend returns full image URL.
    """
    if not logo_url:
        return None
    
    # If already in /uploads/ format, return as is
    if logo_url.startswith("/uploads/"):
        return logo_url
    
    # Remove query parameters if any
    logo_url_clean = logo_url.split('?')[0]
    
    # Extract the filename from the path
    # Handle absolute paths, relative paths, and just filenames
    path_obj = Path(logo_url_clean)
    filename = path_obj.name
    
    # If no filename extracted or it's just a numeric ID, return None
    # Numeric IDs (like "3" or "/images/3") don't have meaningful filenames
    if not filename or filename == logo_url_clean:
        return None
    
    # Check if filename is just a number (numeric ID) - can't create valid file path
    if filename.isdigit():
        return None
    
    # Check if filename has a valid extension (basic validation)
    # If it doesn't look like a file, return None
    if '.' not in filename:
        return None
    
    # Return in /uploads/{filename} format
    return f"/uploads/{filename}"


# ==========================================================
# SAFE CONVERTERS
# ==========================================================
def safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    try:
        result = float(value)
        if result != result or result in (float("inf"), float("-inf")):
            return default
        return result
    except (TypeError, ValueError):
        return default


def safe_str(value, default="", max_length=None, allow_none=False):
    if value is None:
        return None if allow_none else default

    value = str(value).strip()
    if not value:
        return None if allow_none else default

    return value[:max_length] if max_length else value


def safe_json(value, default=None):
    from utils.db_validator import sanitize_json
    return sanitize_json(value, default)


# ==========================================================
# FINAL JSON RESPONSE HELPERS (NO abort())
# ==========================================================
def error_response(message, status_code=400, extra=None):
    """
    Standard JSON error response for APIs.
    Returns a proper JSON response that the frontend can handle.
    This is a pure response helper - no exceptions, no crashes.
    
    Usage:
        return error_response("Property not found", 404)
        return error_response("Invalid input", 400, {"field": "email"})
    """
    payload = {
        "success": False,
        "error": message,
        "code": status_code
    }

    if extra:
        payload.update(extra)

    return jsonify(payload), status_code


def success_response(message=None, data=None, status_code=200):
    """
    Standard JSON success response for APIs.
    
    Usage:
        return success_response("Property deleted successfully")
        return success_response("Property updated", {"id": 123})
        return success_response(data={"properties": [...]})
    """
    payload = {
        "success": True
    }

    if message:
        payload["message"] = message

    if data is not None:
        payload["data"] = data

    return jsonify(payload), status_code


# ==========================================================
# BACKWARD COMPATIBILITY: abort_with_message
# ==========================================================
def abort_with_message(code: int, message: str):
    """
    DEPRECATED: Use error_response() instead.
    Kept for backward compatibility during migration.
    
    IMPORTANT:
    This MUST be returned by the caller.
    Example:
        return abort_with_message(404, "Not found")
    """
    return error_response(message, code)


# ==========================================================
# SESSION VALIDATION
# ==========================================================
def validate_active_session(user_email=None):
    """
    Check if there's an active session in the database for the given user.
    If user_email is provided, only that user's session is valid (fixes logic mismatch:
    frontend thought session expired because we validated "any" session, not this user's).
    Returns (is_valid, session_info) tuple.
    """
    try:
        if user_email:
            active_session_query = """
                SELECT * FROM user_sessions
                WHERE is_active = 1
                AND expires_at > NOW()
                AND LOWER(TRIM(user_email)) = LOWER(TRIM(%s))
                ORDER BY created_at DESC
                LIMIT 1
            """
            active_sessions = execute_query(active_session_query, (user_email,))
        else:
            active_session_query = """
                SELECT * FROM user_sessions
                WHERE is_active = 1
                AND expires_at > NOW()
                ORDER BY created_at DESC
                LIMIT 1
            """
            active_sessions = execute_query(active_session_query)
        if active_sessions and len(active_sessions) > 0:
            active_session = active_sessions[0]
            return (True, {
                "session_id": active_session.get('session_id'),
                "user_id": active_session.get('user_id'),
                "user_email": active_session.get('user_email'),
                "ip_address": active_session.get('ip_address'),
                "created_at": active_session.get('created_at'),
                "expires_at": active_session.get('expires_at')
            })
        return (False, None)
    except Exception as e:
        error_msg = str(e).lower()
        if "table" in error_msg and ("doesn't exist" in error_msg or "unknown table" in error_msg):
            return (False, None)
        print(f"Warning: Error validating session: {str(e)}")
        return (False, None)


# ==========================================================
# ADMIN AUTH DECORATOR — Role-based from DB (no email allowlist)
# 401 = unauthenticated / session expired | 403 = forbidden (not admin)
# ==========================================================
def require_admin_auth(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "OPTIONS":
            return f(*args, **kwargs)

        auth_email = request.headers.get("X-Admin-Email") or request.headers.get("Authorization")
        if auth_email and auth_email.startswith("Email "):
            auth_email = auth_email.replace("Email ", "")
        if not auth_email:
            print("AUTH CHECK FAIL: no X-Admin-Email or Authorization header")
            return error_response("Unauthorized", 401)

        auth_email = auth_email.lower().strip()

        try:
            if not test_connection().get("connected"):
                return error_response("Database unavailable", 500)

            # Look up user by email only; role check is below (403 if not admin)
            user_query = """
                SELECT id, role
                FROM users
                WHERE LOWER(TRIM(email)) = %s
                  AND is_active = 1
                LIMIT 1
            """
            users = execute_query(user_query, (auth_email,))
            if not users:
                print("AUTH CHECK FAIL: user not in DB or inactive", "auth_email:", auth_email)
                return error_response("Unauthorized", 401)

            if (users[0].get("role") or "").lower().strip() != "admin":
                print("AUTH CHECK FAIL: user is not admin (403)", "auth_email:", auth_email, "role:", users[0].get("role"))
                return error_response("Forbidden. Admin access required.", 403)

            has_active_session, session_info = validate_active_session(auth_email)
            if not has_active_session:
                print("AUTH CHECK FAIL: no active session", "auth_email:", auth_email)
                return error_response("Session expired. Please log in again.", 401)
            print("AUTH CHECK OK:", auth_email)

        except Exception:
            traceback.print_exc()
            return error_response("Unauthorized", 401)

        return f(*args, **kwargs)

    return decorated_function
