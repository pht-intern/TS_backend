"""
Authentication routes
"""
from flask import request, jsonify
from datetime import datetime
import os
import json
import traceback
from database import test_connection, execute_query, execute_update, get_db_cursor
from schemas import LoginSchema, LoginResponseSchema
from utils.auth import verify_password
from utils.helpers import get_client_ip, abort_with_message


def register_auth_routes(app):
    """Register authentication routes"""
    
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
            
            # Query user from database
            try:
                user_query = "SELECT * FROM users WHERE email = %s AND is_active = 1 AND role = 'admin'"
                users = execute_query(user_query, (login_data.email,))
            except Exception as db_error:
                error_msg = str(db_error)
                print(f"Database query error during login: {error_msg}")
                traceback.print_exc()
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
                print(f"Warning: Failed to update last_login timestamp: {str(update_error)}")
            
            # Log successful login to activity logs
            try:
                ip_address = get_client_ip()
                user_agent = request.headers.get("User-Agent", None)
                login_log_query = "INSERT INTO logs (log_type, action, description, user_email, ip_address, user_agent, metadata) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                login_metadata = {
                    "login_timestamp": datetime.now().isoformat(),
                    "user_id": user['id'],
                    "user_role": user.get('role', 'admin'),
                    "login_method": "email_password"
                }
                login_metadata_json = json.dumps(login_metadata)
                with get_db_cursor() as cursor:
                    cursor.execute(login_log_query, (
                        'action',
                        'user_login',
                        f"User logged in: {user['email']}",
                        user['email'],
                        ip_address,
                        user_agent,
                        login_metadata_json
                    ))
            except Exception as log_error:
                print(f"Warning: Failed to log login activity: {str(log_error)}")
            
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
            if "Access denied" in error_msg or "(1045" in error_msg:
                abort_with_message(500, "Database authentication failed. Please verify DB_USER and DB_PASSWORD in cPanel environment variables.")
            elif "Can't connect" in error_msg or "Connection refused" in error_msg:
                abort_with_message(500, "Cannot connect to database server. Please verify DB_HOST in cPanel environment variables.")
            elif "Unknown database" in error_msg:
                abort_with_message(500, "Database not found. Please verify DB_NAME in cPanel environment variables.")
            else:
                abort_with_message(500, f"An error occurred during login: {error_msg}")
