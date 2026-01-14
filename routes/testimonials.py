"""
Testimonials routes
"""
from flask import request, jsonify, make_response
import json
import re
import traceback
from database import execute_query
from schemas import TestimonialPublicSchema
from utils.helpers import abort_with_message


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
