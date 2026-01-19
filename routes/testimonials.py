"""
Testimonials routes
"""
from flask import request, jsonify, make_response
import json
import re
import traceback
from database import execute_query, execute_update, execute_insert
from schemas import TestimonialPublicSchema, TestimonialResponseSchema, TestimonialUpdateSchema, TestimonialCreateSchema
from utils.helpers import abort_with_message, require_admin_auth


def register_testimonials_routes(app):
    """Register testimonials routes"""
    
    @app.route("/api/testimonials", methods=["GET"])
    def get_testimonials():
        """Get all testimonials (public endpoint - only approved)"""
        try:
            # Parse is_approved parameter (default to True for approved testimonials)
            is_approved_param = request.args.get('is_approved', default='true')
            is_approved = str(is_approved_param).lower() == 'true'
            
            # Parse is_featured parameter (optional)
            is_featured_param = request.args.get('is_featured')
            is_featured = None
            if is_featured_param is not None:
                is_featured = str(is_featured_param).lower() == 'true'
            
            is_approved_int = 1 if is_approved else 0
            conditions = ["is_approved = %s"]
            params = [is_approved_int]
            
            if is_featured is not None:
                is_featured_int = 1 if is_featured else 0
                conditions.append("is_featured = %s")
                params.append(is_featured_int)
            
            where_clause = " AND ".join(conditions)
            query = f"SELECT * FROM testimonials WHERE {where_clause} ORDER BY created_at DESC"
            
            print(f"Testimonials query: {query}")
            print(f"Query params: {params}")
            
            testimonials = execute_query(query, tuple(params))
            
            print(f"Found {len(testimonials)} testimonials")
            
            result = []
            for t in testimonials:
                try:
                    testimonial_dict = dict(t)
                    if 'is_featured' not in testimonial_dict:
                        testimonial_dict['is_featured'] = False
                    if 'created_at' not in testimonial_dict:
                        testimonial_dict['created_at'] = None
                    result.append(TestimonialPublicSchema(**testimonial_dict))
                except Exception as schema_error:
                    print(f"Error converting testimonial {t.get('id', 'unknown')}: {str(schema_error)}")
                    continue
            
            data = [r.dict() for r in result]
            
            # Support JSONP if callback parameter is provided
            callback = request.args.get('callback')
            if callback:
                # Validate callback name to prevent XSS
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({json.dumps(data)});")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
                else:
                    # Invalid callback name, return regular JSON
                    return jsonify({'error': 'Invalid callback parameter'}), 400
            
            return jsonify(data)
        except Exception as e:
            error_msg = str(e)
            print(f"Error fetching testimonials: {error_msg}")
            traceback.print_exc()
            # Support JSONP even for errors
            callback = request.args.get('callback')
            if callback:
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}([]);")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
            abort_with_message(500, f"Error fetching testimonials: {error_msg}")
    
    @app.route("/api/testimonials", methods=["POST"])
    @require_admin_auth
    def create_testimonial():
        """Create a new testimonial"""
        try:
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
            testimonial_data = TestimonialCreateSchema(**data)
            
            insert_query = """
                INSERT INTO testimonials (
                    client_name, client_email, client_phone, service_type, 
                    rating, message, is_approved, is_featured
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            testimonial_id = execute_insert(insert_query, (
                testimonial_data.client_name,
                testimonial_data.client_email,
                testimonial_data.client_phone,
                testimonial_data.service_type,
                testimonial_data.rating,
                testimonial_data.message,
                1 if testimonial_data.is_approved else 0,
                1 if testimonial_data.is_featured else 0
            ))
            
            # Return the created testimonial
            result = execute_query("SELECT * FROM testimonials WHERE id = %s", (testimonial_id,))
            testimonial_dict = dict(result[0])
            
            # Ensure all required fields are present
            if 'is_featured' not in testimonial_dict:
                testimonial_dict['is_featured'] = False
            if 'created_at' not in testimonial_dict:
                testimonial_dict['created_at'] = None
            
            response = TestimonialResponseSchema(**testimonial_dict)
            return jsonify(response.dict()), 201
        except Exception as e:
            print(f"Error creating testimonial: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error creating testimonial: {str(e)}")
    
    @app.route("/api/admin/testimonials", methods=["GET"])
    @require_admin_auth
    def get_all_testimonials():
        """Get all testimonials (admin endpoint - includes unapproved)"""
        try:
            testimonials = execute_query("SELECT * FROM testimonials ORDER BY created_at DESC")
            result = [TestimonialResponseSchema(**dict(t)) for t in testimonials]
            return jsonify([r.dict() for r in result])
        except Exception as e:
            print(f"Error fetching testimonials: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching testimonials: {str(e)}")
    
    @app.route("/api/testimonials/<int:testimonial_id>", methods=["POST"])
    @require_admin_auth
    def update_testimonial(testimonial_id: int):
        """Update a testimonial"""
        try:
            existing = execute_query("SELECT id FROM testimonials WHERE id = %s", (testimonial_id,))
            if not existing:
                abort_with_message(404, "Testimonial not found")
            
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
            testimonial_data = TestimonialUpdateSchema(**data)
            
            updates = []
            params = []
            
            if testimonial_data.client_name is not None:
                updates.append("client_name = %s")
                params.append(testimonial_data.client_name)
            if testimonial_data.client_email is not None:
                updates.append("client_email = %s")
                params.append(testimonial_data.client_email)
            if testimonial_data.client_phone is not None:
                updates.append("client_phone = %s")
                params.append(testimonial_data.client_phone)
            if testimonial_data.service_type is not None:
                updates.append("service_type = %s")
                params.append(testimonial_data.service_type)
            if testimonial_data.rating is not None:
                updates.append("rating = %s")
                params.append(testimonial_data.rating)
            if testimonial_data.message is not None:
                updates.append("message = %s")
                params.append(testimonial_data.message)
            if testimonial_data.is_approved is not None:
                updates.append("is_approved = %s")
                params.append(1 if testimonial_data.is_approved else 0)
            if testimonial_data.is_featured is not None:
                updates.append("is_featured = %s")
                params.append(1 if testimonial_data.is_featured else 0)
            
            if updates:
                params.append(testimonial_id)
                update_query = f"UPDATE testimonials SET {', '.join(updates)} WHERE id = %s"
                execute_update(update_query, tuple(params))
            
            result = execute_query("SELECT * FROM testimonials WHERE id = %s", (testimonial_id,))
            response = TestimonialResponseSchema(**dict(result[0]))
            return jsonify(response.dict())
        except Exception as e:
            print(f"Error updating testimonial: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error updating testimonial: {str(e)}")
    
    @app.route("/api/testimonials/<int:testimonial_id>", methods=["DELETE"])
    @require_admin_auth
    def delete_testimonial(testimonial_id: int):
        """Delete a testimonial"""
        try:
            result = execute_update("DELETE FROM testimonials WHERE id = %s", (testimonial_id,))
            if result == 0:
                abort_with_message(404, "Testimonial not found")
            return jsonify({"message": "Testimonial deleted successfully"})
        except Exception as e:
            print(f"Error deleting testimonial: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error deleting testimonial: {str(e)}")
