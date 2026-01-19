"""
Contact inquiries routes
"""
from flask import request, jsonify
import traceback
import threading
from database import execute_query, execute_update, execute_insert
from schemas import (
    ContactInquiryCreateSchema, ContactInquiryUpdateSchema, ContactInquiryResponseSchema
)
from models import InquiryStatus
from utils.helpers import abort_with_message, get_client_ip, require_admin_auth
from utils.email import send_schedule_visit_email, send_self_notification_email, parse_visit_details_from_message


def register_inquiries_routes(app):
    """Register inquiries routes"""
    
    @app.route("/api/contact", methods=["POST"])
    def create_inquiry():
        """Create a new contact inquiry"""
        try:
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
            inquiry_data = ContactInquiryCreateSchema(**data)
            
            # Get client IP address
            ip_address = get_client_ip()
            
            query = """
                INSERT INTO contact_inquiries (name, email, subject, message, phone, property_id, status, ip_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            inquiry_id = execute_insert(query, (
                inquiry_data.name, inquiry_data.email, inquiry_data.subject,
                inquiry_data.message, inquiry_data.phone, inquiry_data.property_id,
                InquiryStatus.NEW.value, ip_address
            ))
            
            # Send email notification if this is a Schedule Visit request
            if inquiry_data.subject and inquiry_data.subject.lower() == "schedule visit":
                visit_date, visit_time, additional_notes = parse_visit_details_from_message(inquiry_data.message)
                
                def send_email():
                    send_schedule_visit_email(
                        inquiry_data.name,
                        inquiry_data.email,
                        inquiry_data.phone,
                        visit_date,
                        visit_time,
                        inquiry_data.message,
                        inquiry_data.property_id
                    )
                
                thread = threading.Thread(target=send_email)
                thread.daemon = True
                thread.start()
            
            # Send self-notification email for all contact inquiries
            def send_notification():
                property_title = ""
                if inquiry_data.property_id:
                    try:
                        # Check residential_properties first
                        properties = execute_query("SELECT property_name as title FROM residential_properties WHERE id = %s", (inquiry_data.property_id,))
                        if not properties or len(properties) == 0:
                            # Check plot_properties if not found in residential
                            properties = execute_query("SELECT project_name as title FROM plot_properties WHERE id = %s", (inquiry_data.property_id,))
                        if properties and len(properties) > 0:
                            property_title = properties[0]['title']
                    except Exception:
                        pass
                
                if inquiry_data.subject and inquiry_data.subject.lower() == "schedule visit":
                    notification_title = "New Schedule Visit Request"
                    notification_message = f"A new schedule visit request has been received from {inquiry_data.name}. Please check your dashboard to manage this request."
                else:
                    notification_title = "New Contact Inquiry"
                    notification_message = f"A new contact inquiry has been received from {inquiry_data.name}. Please check your dashboard to respond."
                
                send_self_notification_email(
                    "new_inquiry",
                    notification_title,
                    notification_message,
                    {
                        "Inquirer Name": inquiry_data.name,
                        "Inquirer Email": inquiry_data.email,
                        "Inquirer Phone": inquiry_data.phone or "Not provided",
                        "Subject": inquiry_data.subject or "No subject",
                        "Property": property_title or "General inquiry",
                        "Inquiry ID": inquiry_id,
                        "Status": "New"
                    }
                )
            
            thread = threading.Thread(target=send_notification)
            thread.daemon = True
            thread.start()
            
            result = execute_query("SELECT * FROM contact_inquiries WHERE id = %s", (inquiry_id,))
            response = ContactInquiryResponseSchema(**dict(result[0]))
            return jsonify(response.dict()), 201
        except Exception as e:
            print(f"Error creating inquiry: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error creating inquiry: {str(e)}")
    
    @app.route("/api/admin/inquiries", methods=["GET"])
    @require_admin_auth
    def get_inquiries():
        """Get all contact inquiries (admin endpoint)"""
        try:
            status_str = request.args.get('status')
            status = None
            if status_str:
                try:
                    status = InquiryStatus(status_str)
                except ValueError:
                    pass
            
            if status:
                query = "SELECT * FROM contact_inquiries WHERE status = %s ORDER BY created_at DESC"
                inquiries = execute_query(query, (status.value,))
            else:
                query = "SELECT * FROM contact_inquiries ORDER BY created_at DESC"
                inquiries = execute_query(query)
            
            result = [ContactInquiryResponseSchema(**dict(i)) for i in inquiries]
            return jsonify([r.dict() for r in result])
        except Exception as e:
            print(f"Error fetching inquiries: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching inquiries: {str(e)}")
    
    @app.route("/api/admin/inquiries/<int:inquiry_id>", methods=["POST"])
    @require_admin_auth
    def update_inquiry(inquiry_id: int):
        """Update a contact inquiry"""
        try:
            existing = execute_query("SELECT id FROM contact_inquiries WHERE id = %s", (inquiry_id,))
            if not existing:
                abort_with_message(404, "Inquiry not found")
            
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
            inquiry_data = ContactInquiryUpdateSchema(**data)
            
            updates = []
            params = []
            
            if inquiry_data.name is not None:
                updates.append("name = %s")
                params.append(inquiry_data.name)
            if inquiry_data.email is not None:
                updates.append("email = %s")
                params.append(inquiry_data.email)
            if inquiry_data.subject is not None:
                updates.append("subject = %s")
                params.append(inquiry_data.subject)
            if inquiry_data.message is not None:
                updates.append("message = %s")
                params.append(inquiry_data.message)
            if inquiry_data.phone is not None:
                updates.append("phone = %s")
                params.append(inquiry_data.phone)
            if inquiry_data.property_id is not None:
                updates.append("property_id = %s")
                params.append(inquiry_data.property_id)
            if inquiry_data.status is not None:
                updates.append("status = %s")
                params.append(inquiry_data.status.value)
            
            if updates:
                params.append(inquiry_id)
                update_query = f"UPDATE contact_inquiries SET {', '.join(updates)} WHERE id = %s"
                execute_update(update_query, tuple(params))
            
            result = execute_query("SELECT * FROM contact_inquiries WHERE id = %s", (inquiry_id,))
            response = ContactInquiryResponseSchema(**dict(result[0]))
            return jsonify(response.dict())
        except Exception as e:
            print(f"Error updating inquiry: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error updating inquiry: {str(e)}")
