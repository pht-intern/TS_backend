"""
Visitor info routes
"""
from flask import request, jsonify
import traceback
import threading
from database import execute_query, execute_insert
from schemas import VisitorInfoCreateSchema, VisitorInfoResponseSchema
from utils.helpers import abort_with_message, require_admin_auth, get_client_ip
from utils.email import send_self_notification_email


def register_visitor_info_routes(app):
    """Register visitor info routes"""
    
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
            visitor_id = execute_insert(query, (
                visitor_data.full_name, visitor_data.email,
                visitor_data.phone, visitor_data.looking_for, ip_address
            ))
            
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
