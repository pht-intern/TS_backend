"""
Logs routes
"""
from flask import request, jsonify
from datetime import datetime
import json
import traceback
from database import get_db_cursor
from schemas import LogCreateSchema
from utils.helpers import get_client_ip


def register_logs_routes(app):
    """Register logs routes"""
    
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
                return jsonify({
                    "success": True,
                    "message": "Log created successfully"
                })
            except Exception as db_error:
                # Log error but don't fail the request
                print(f"Warning: Could not create log entry: {str(db_error)}")
                traceback.print_exc()
                return jsonify({
                    "success": True,
                    "message": "Log entry accepted (may not be persisted)"
                })
        except Exception as e:
            # Always return success to prevent frontend errors
            print(f"Warning: Error in create_log endpoint: {str(e)}")
            traceback.print_exc()
            return jsonify({
                "success": True,
                "message": "Log entry accepted"
            })
