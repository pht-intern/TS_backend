"""
Cities routes
"""
from flask import request, jsonify, make_response
import json
import re
import traceback
from database import execute_query
from utils.helpers import abort_with_message


def register_cities_routes(app):
    """Register cities routes"""
    
    @app.route("/api/cities", methods=["GET"])
    def get_active_cities():
        """Get all active cities (public endpoint)"""
        try:
            query = """
                SELECT 
                    c.name,
                    c.state
                FROM cities c
                WHERE c.is_active = 1
                ORDER BY c.state, c.name
            """
            cities = execute_query(query)
            data = {
                "success": True,
                "cities": cities or []
            }
            
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
            print(f"Error fetching active cities: {str(e)}")
            traceback.print_exc()
            # Support JSONP even for errors
            callback = request.args.get('callback')
            if callback:
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({{'success': False, 'cities': []}});")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
            abort_with_message(500, f"Error fetching active cities: {str(e)}")
