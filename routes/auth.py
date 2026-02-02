"""
Authentication routes
"""
from flask import request, jsonify
from datetime import datetime, timedelta
import os
import json
import traceback
import uuid
from database import test_connection, execute_query, execute_update, get_db_cursor
from schemas import LoginSchema, LoginResponseSchema
from utils.auth import verify_password
from utils.helpers import get_client_ip, abort_with_message


def register_auth_routes(app):
    """Register authentication routes"""
    
    @app.route("/api/auth/login", methods=["POST"])
    def login():
        """User login endpoint - Only allows one active session at a time"""
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
            
            # CRITICAL: Check for active sessions - only one session allowed at a time
            ip_address = get_client_ip()
            try:
                # Check if there's an active session (not expired)
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
                    active_ip = active_session.get('ip_address', 'Unknown')
                    active_email = active_session.get('user_email', 'Unknown')
                    
                    # Block login if there's already an active session
                    # Even if it's the same IP, we only allow one session
                    abort_with_message(403, f"Another session is already active. Only one user can be logged in at a time. Active session from IP: {active_ip}")
            except Exception as session_check_error:
                # If table doesn't exist, create it and continue
                error_msg = str(session_check_error).lower()
                if "table" in error_msg and "doesn't exist" in error_msg or "unknown table" in error_msg:
                    print("user_sessions table not found, creating it...")
                    try:
                        create_sessions_table = """
                            CREATE TABLE IF NOT EXISTS user_sessions (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                session_id VARCHAR(255) NOT NULL UNIQUE,
                                user_id INT NOT NULL,
                                user_email VARCHAR(255) NOT NULL,
                                ip_address VARCHAR(45) NOT NULL,
                                user_agent TEXT,
                                is_active TINYINT(1) DEFAULT 1,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                expires_at TIMESTAMP NOT NULL,
                                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                INDEX idx_session_id (session_id),
                                INDEX idx_user_id (user_id),
                                INDEX idx_is_active (is_active),
                                INDEX idx_expires_at (expires_at),
                                INDEX idx_active_expires (is_active, expires_at),
                                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                        """
                        execute_update(create_sessions_table)
                        print("✓ user_sessions table created successfully")
                    except Exception as create_error:
                        print(f"Warning: Could not create user_sessions table: {str(create_error)}")
                        # Continue with login even if table creation fails
                else:
                    print(f"Warning: Error checking active sessions: {str(session_check_error)}")
                    # Continue with login, but log the error
            
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
            
            # Require non-empty password
            if not login_data.password or not str(login_data.password).strip():
                abort_with_message(400, "Password is required")
            
            # Get password_hash from row (MySQL may return column names in different case)
            stored_hash = None
            for key, value in user.items():
                if key and str(key).lower() == "password_hash" and value:
                    stored_hash = value
                    break
            if not stored_hash or not isinstance(stored_hash, str):
                abort_with_message(401, "Invalid email or password")
            
            if not verify_password(login_data.password.strip(), stored_hash):
                abort_with_message(401, "Invalid email or password")
            
            # Double-check user has admin role
            if user.get('role') != 'admin':
                abort_with_message(403, "Access denied: Admin role required")
            
            # Create new session - deactivate any old sessions first
            session_id = str(uuid.uuid4())
            session_timeout_hours = int(os.getenv("SESSION_TIMEOUT_HOURS", "4"))
            expires_at = datetime.now() + timedelta(hours=session_timeout_hours)
            
            try:
                # Deactivate all existing sessions for this user (safety measure)
                deactivate_query = "UPDATE user_sessions SET is_active = 0 WHERE user_id = %s AND is_active = 1"
                execute_update(deactivate_query, (user['id'],))
                
                # Create new session
                user_agent = request.headers.get("User-Agent", None)
                create_session_query = """
                    INSERT INTO user_sessions 
                    (session_id, user_id, user_email, ip_address, user_agent, is_active, expires_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                execute_update(create_session_query, (
                    session_id,
                    user['id'],
                    user['email'],
                    ip_address,
                    user_agent,
                    1,
                    expires_at
                ))
            except Exception as session_error:
                print(f"Warning: Failed to create session: {str(session_error)}")
                # Continue with login even if session creation fails
                # But log it for debugging
                traceback.print_exc()
            
            # Update last login timestamp
            try:
                update_query = "UPDATE users SET last_login = %s WHERE id = %s"
                execute_update(update_query, (datetime.now(), user['id']))
            except Exception as update_error:
                print(f"Warning: Failed to update last_login timestamp: {str(update_error)}")
            
            # Log successful login to activity logs
            try:
                user_agent = request.headers.get("User-Agent", None)
                login_log_query = "INSERT INTO logs (log_type, action, description, user_email, ip_address, user_agent, metadata) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                login_metadata = {
                    "login_timestamp": datetime.now().isoformat(),
                    "user_id": user['id'],
                    "user_role": user.get('role', 'admin'),
                    "login_method": "email_password",
                    "session_id": session_id,
                    "ip_address": ip_address
                }
                login_metadata_json = json.dumps(login_metadata)
                with get_db_cursor() as cursor:
                    cursor.execute(login_log_query, (
                        'action',
                        'user_login',
                        f"User logged in: {user['email']} from IP: {ip_address}",
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
    
    @app.route("/api/auth/logout", methods=["POST"])
    def logout():
        """User logout endpoint - clears active session"""
        try:
            ip_address = get_client_ip()
            user_agent = request.headers.get("User-Agent", None)
            
            # Get user email from request if available
            data = request.get_json() or {}
            user_email = data.get('email', None)
            
            # Deactivate all active sessions
            try:
                if user_email:
                    # Deactivate sessions for specific user
                    deactivate_query = """
                        UPDATE user_sessions 
                        SET is_active = 0 
                        WHERE user_email = %s AND is_active = 1
                    """
                    execute_update(deactivate_query, (user_email,))
                else:
                    # Deactivate all active sessions (fallback)
                    deactivate_query = "UPDATE user_sessions SET is_active = 0 WHERE is_active = 1"
                    execute_update(deactivate_query)
            except Exception as session_error:
                # If table doesn't exist, that's okay - just log it
                error_msg = str(session_error).lower()
                if "table" in error_msg and "doesn't exist" in error_msg or "unknown table" in error_msg:
                    print("user_sessions table not found during logout - this is okay if it hasn't been created yet")
                else:
                    print(f"Warning: Failed to deactivate session during logout: {str(session_error)}")
            
            # Log logout activity
            if user_email:
                try:
                    logout_log_query = "INSERT INTO logs (log_type, action, description, user_email, ip_address, user_agent, metadata) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    logout_metadata = {
                        "logout_timestamp": datetime.now().isoformat(),
                        "logout_method": "explicit",
                        "ip_address": ip_address
                    }
                    logout_metadata_json = json.dumps(logout_metadata)
                    with get_db_cursor() as cursor:
                        cursor.execute(logout_log_query, (
                            'action',
                            'user_logout',
                            f"User logged out: {user_email}",
                            user_email,
                            ip_address,
                            user_agent,
                            logout_metadata_json
                        ))
                except Exception as log_error:
                    print(f"Warning: Failed to log logout activity: {str(log_error)}")
            
            return jsonify({
                "success": True,
                "message": "Logout successful"
            })
        except Exception as e:
            error_msg = str(e)
            print(f"Logout error: {error_msg}")
            traceback.print_exc()
            return jsonify({
                "success": False,
                "error": "An error occurred during logout"
            }), 500
    
    @app.route("/api/auth/check-session", methods=["GET"])
    def check_session():
        """Check if there's an active session"""
        try:
            # Check for active sessions
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
                return jsonify({
                    "success": True,
                    "has_active_session": True,
                    "session": {
                        "user_email": active_session.get('user_email'),
                        "ip_address": active_session.get('ip_address'),
                        "created_at": active_session.get('created_at').isoformat() if active_session.get('created_at') else None,
                        "expires_at": active_session.get('expires_at').isoformat() if active_session.get('expires_at') else None
                    }
                })
            else:
                return jsonify({
                    "success": True,
                    "has_active_session": False
                })
        except Exception as e:
            # If table doesn't exist, return no active session
            error_msg = str(e).lower()
            if "table" in error_msg and "doesn't exist" in error_msg or "unknown table" in error_msg:
                return jsonify({
                    "success": True,
                    "has_active_session": False
                })
            print(f"Error checking session: {str(e)}")
            return jsonify({
                "success": False,
                "error": "Error checking session status"
            }), 500