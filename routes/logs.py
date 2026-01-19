"""
Logs routes
"""
from flask import request, jsonify
from datetime import datetime
import json
import traceback
from database import get_db_cursor, execute_query
from schemas import LogCreateSchema, LogResponseSchema
from utils.helpers import get_client_ip, abort_with_message, require_admin_auth


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
                        if isinstance(log['metadata'], str):
                            log['metadata'] = json.loads(log['metadata'])
                    except:
                        log['metadata'] = None
            
            result = [LogResponseSchema(**dict(log)) for log in logs]
            return jsonify([r.dict() for r in result])
        except Exception as e:
            print(f"Error fetching logs: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching logs: {str(e)}")
