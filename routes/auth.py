"""
Authentication routes
"""
from flask import request, jsonify
from datetime import datetime, timedelta
import os
import json
import traceback
import uuid

from database import (
    test_connection,
    execute_query,
    execute_update,
    get_db_cursor
)
from schemas import LoginSchema, LoginResponseSchema
from utils.auth import verify_password
from utils.helpers import get_client_ip, abort_with_message


def register_auth_routes(app):

    # -------------------------
    # LOGIN
    # -------------------------
    @app.route("/api/auth/login", methods=["POST"])
    def login():
        try:
            data = request.get_json()
            if not data:
                return abort_with_message(400, "Invalid request data")

            # Validate payload
            try:
                login_data = LoginSchema(**data)
            except Exception as e:
                return abort_with_message(400, str(e))

            # Check DB connection
            connection_test = test_connection()
            if not connection_test.get("connected"):
                return abort_with_message(
                    500,
                    "Database connection failed. Please check configuration."
                )

            # -------------------------
            # FETCH USER FIRST
            # -------------------------
            user_query = """
                SELECT *
                FROM users
                WHERE email = %s
                  AND is_active = 1
                  AND role = 'admin'
                LIMIT 1
            """
            users = execute_query(user_query, (login_data.email,))
            if not users:
                return abort_with_message(401, "Invalid email or password")

            user = users[0]

            # Verify password
            stored_hash = user.get("password_hash")
            if not stored_hash or not verify_password(login_data.password, stored_hash):
                return abort_with_message(401, "Invalid email or password")

            # -------------------------
            # CHECK ACTIVE SESSION (USER-SCOPED)
            # -------------------------
            active_session_query = """
                SELECT session_id, ip_address
                FROM user_sessions
                WHERE user_id = %s
                  AND is_active = 1
                  AND expires_at > NOW()
                LIMIT 1
            """
            active_sessions = execute_query(active_session_query, (user["id"],))

            if active_sessions:
                return abort_with_message(
                    403,
                    "You are already logged in from another session."
                )

            # -------------------------
            # CREATE NEW SESSION
            # -------------------------
            session_id = str(uuid.uuid4())
            ip_address = get_client_ip()
            user_agent = request.headers.get("User-Agent")
            timeout_hours = int(os.getenv("SESSION_TIMEOUT_HOURS", "4"))
            expires_at = datetime.now() + timedelta(hours=timeout_hours)

            try:
                # Deactivate any old sessions (safety)
                execute_update(
                    "UPDATE user_sessions SET is_active = 0 WHERE user_id = %s",
                    (user["id"],)
                )

                # Insert new active session
                insert_session_query = """
                    INSERT INTO user_sessions (
                        session_id,
                        user_id,
                        user_email,
                        ip_address,
                        user_agent,
                        is_active,
                        created_at,
                        expires_at,
                        last_activity
                    ) VALUES (%s, %s, %s, %s, %s, 1, NOW(), %s, NOW())
                """
                execute_update(insert_session_query, (
                    session_id,
                    user["id"],
                    user["email"],
                    ip_address,
                    user_agent,
                    expires_at
                ))
            except Exception:
                traceback.print_exc()
                return abort_with_message(500, "Failed to create session")

            # Update last login
            execute_update(
                "UPDATE users SET last_login = %s WHERE id = %s",
                (datetime.now(), user["id"])
            )

            # Log login
            try:
                metadata = json.dumps({
                    "session_id": session_id,
                    "ip_address": ip_address,
                    "user_id": user["id"]
                })
                with get_db_cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO logs
                        (log_type, action, description, user_email, ip_address, user_agent, metadata)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            "action",
                            "user_login",
                            f"User logged in from {ip_address}",
                            user["email"],
                            ip_address,
                            user_agent,
                            metadata
                        )
                    )
            except Exception:
                traceback.print_exc()

            # Send actual role and is_admin from DB so non-admin users (is_admin=0) redirect to dashboard
            user_role = user.get("role") or "admin"
            is_admin = user.get("is_admin") in (1, True) or user.get("is_admin") == "1"
            response = LoginResponseSchema(
                success=True,
                message="Login successful",
                token=None,
                user={
                    "id": user["id"],
                    "email": user["email"],
                    "full_name": user.get("full_name"),
                    "role": user_role,
                    "is_admin": bool(is_admin)
                }
            )
            return jsonify(response.model_dump())

        except Exception as e:
            traceback.print_exc()
            return abort_with_message(500, f"Login failed: {str(e)}")

    # -------------------------
    # LOGOUT
    # -------------------------
    @app.route("/api/auth/logout", methods=["POST"])
    def logout():
        try:
            data = request.get_json() or {}
            user_email = data.get("email")

            if user_email:
                execute_update(
                    "UPDATE user_sessions SET is_active = 0 WHERE user_email = %s",
                    (user_email,)
                )
            else:
                execute_update(
                    "UPDATE user_sessions SET is_active = 0 WHERE is_active = 1"
                )

            # End expired sessions properly: mark as inactive for DB hygiene (production/cPanel)
            try:
                execute_update(
                    "UPDATE user_sessions SET is_active = 0 WHERE expires_at <= NOW()"
                )
            except Exception:
                pass  # Non-fatal; table may not exist in some envs

            return jsonify({
                "success": True,
                "message": "Logout successful"
            })

        except Exception:
            traceback.print_exc()
            return abort_with_message(500, "Logout failed")

    # -------------------------
    # CHECK SESSION (OPTIONAL)
    # -------------------------
    @app.route("/api/auth/check-session", methods=["GET"])
    def check_session():
        try:
            print("AUTH CHECK-SESSION: called")
            query = """
                SELECT user_email, ip_address, created_at, expires_at
                FROM user_sessions
                WHERE is_active = 1
                  AND expires_at > NOW()
                ORDER BY created_at DESC
                LIMIT 1
            """
            sessions = execute_query(query)
            print("AUTH CHECK-SESSION: sessions count:", len(sessions) if sessions else 0, "user_email:", sessions[0].get("user_email") if sessions else None)

            if sessions:
                s = sessions[0]
                return jsonify({
                    "success": True,
                    "has_active_session": True,
                    "session": {
                        "user_email": s["user_email"],
                        "ip_address": s["ip_address"],
                        "created_at": s["created_at"].isoformat(),
                        "expires_at": s["expires_at"].isoformat()
                    }
                })

            return jsonify({
                "success": True,
                "has_active_session": False
            })

        except Exception:
            traceback.print_exc()
            return abort_with_message(500, "Failed to check session")
