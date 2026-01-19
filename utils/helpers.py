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
def save_base64_image(base64_string: str, images_dir: Path = None) -> str:
    if not base64_string or not base64_string.startswith("data:image/"):
        return base64_string

    try:
        if images_dir is None:
            from config import IMAGES_DIR
            images_dir = IMAGES_DIR

        header, data = base64_string.split(",", 1)
        image_format = header.split("/")[1].split(";")[0]
        image_data = base64.b64decode(data)

        if images_dir.name == "images":
            target_dir = images_dir / "properties"
        else:
            target_dir = images_dir / "images" / "properties"

        target_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid.uuid4()}.{image_format}"
        file_path = target_dir / filename

        with open(file_path, "wb") as f:
            f.write(image_data)

        return f"/images/properties/{filename}"

    except Exception as e:
        print(f"Image save failed: {e}")
        return base64_string


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

    if "/public_html/" in url:
        url = "/" + url.split("/public_html/", 1)[1].lstrip("/")

    if "/images/" in url:
        url = url[url.rfind("/images/"):]

    return url if url.startswith("/images/") else f"/images/{url.lstrip('/')}"


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
# FINAL JSON ERROR RESPONSE (NO abort())
# ==========================================================
def abort_with_message(code: int, message: str):
    """
    IMPORTANT:
    This MUST be returned by the caller.
    Example:
        return abort_with_message(404, "Not found")
    """
    return jsonify({
        "success": False,
        "error": message,
        "code": code
    }), code


# ==========================================================
# ADMIN AUTH DECORATOR (FINAL & SAFE)
# ==========================================================
def require_admin_auth(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        allowed_admin_email = os.getenv("ADMIN_EMAIL")
        if not allowed_admin_email:
            return abort_with_message(500, "Server configuration error")

        auth_email = request.headers.get("X-Admin-Email") or request.headers.get("Authorization")

        if auth_email and auth_email.startswith("Email "):
            auth_email = auth_email.replace("Email ", "")

        if not auth_email:
            return abort_with_message(401, "Unauthorized")

        auth_email = auth_email.lower().strip()
        allowed_admin_email = allowed_admin_email.lower().strip()

        if auth_email != allowed_admin_email:
            return abort_with_message(401, "Unauthorized")

        try:
            if not test_connection().get("connected"):
                return abort_with_message(500, "Database unavailable")

            user_query = """
                SELECT id
                FROM users
                WHERE email = %s
                  AND role = 'admin'
                  AND is_active = 1
                LIMIT 1
            """
            users = execute_query(user_query, (auth_email,))
            if not users:
                return abort_with_message(401, "Unauthorized")

        except Exception:
            traceback.print_exc()
            return abort_with_message(401, "Unauthorized")

        return f(*args, **kwargs)

    return decorated_function
