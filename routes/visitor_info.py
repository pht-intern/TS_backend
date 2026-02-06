"""
Visitor info routes
"""
from flask import request, jsonify, session
import traceback
import threading
from database import execute_query, execute_insert
from schemas import VisitorInfoCreateSchema, VisitorInfoResponseSchema
from utils.helpers import abort_with_message, require_admin_auth, get_client_ip
from utils.email import send_self_notification_email


def register_visitor_info_routes(app):
    """Register visitor info routes"""
    
    @app.route("/api/visitor-info/check", methods=["GET"])
    def check_visitor_submitted():
        """Check if visitor has already submitted the form (based on session/IP)"""
        try:
            # Get client IP address
            ip_address = get_client_ip()
            
            # Check session first (faster)
            if session.get('visitor_form_submitted'):
                return jsonify({
                    'submitted': True,
                    'message': 'Visitor form already submitted in this session'
                }), 200
            
            # Also check database for this IP address (in case session expired but same IP)
            # This prevents showing modal again even if session is cleared
            ip_check_query = "SELECT COUNT(*) as count FROM visitor_info WHERE ip_address = %s"
            ip_result = execute_query(ip_check_query, (ip_address,))
            
            if ip_result and len(ip_result) > 0 and ip_result[0].get('count', 0) > 0:
                # IP found in database, mark session so we don't check DB again
                session['visitor_form_submitted'] = True
                session['visitor_ip'] = ip_address
                return jsonify({
                    'submitted': True,
                    'message': 'Visitor form already submitted from this IP address'
                }), 200
            
            return jsonify({
                'submitted': False,
                'message': 'Visitor form not submitted yet'
            }), 200
        except Exception as e:
            print(f"Error checking visitor submission: {str(e)}")
            traceback.print_exc()
            # On error, allow modal to show (fail open)
            return jsonify({
                'submitted': False,
                'message': 'Error checking submission status'
            }), 200
    
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
            
            # Check if already submitted in this session
            if session.get('visitor_form_submitted'):
                return jsonify({
                    'message': 'Form already submitted',
                    'submitted': True
                }), 200
            
            query = "INSERT INTO visitor_info (full_name, email, phone, looking_for, ip_address) VALUES (%s, %s, %s, %s, %s)"
            visitor_id = execute_insert(query, (
                visitor_data.full_name, visitor_data.email,
                visitor_data.phone, visitor_data.looking_for, ip_address
            ))
            
            # Mark session as submitted to prevent showing modal again
            session['visitor_form_submitted'] = True
            session['visitor_ip'] = ip_address
            # Make session permanent so it persists across browser restarts
            session.permanent = True
            
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
                        "Visitor ID": visitor_id,
                        "IP Address": ip_address
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
