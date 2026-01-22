"""
Categories routes
"""
from flask import request, jsonify, make_response
from datetime import datetime
import json
import re
import traceback
from database import execute_query, execute_insert
from utils.helpers import abort_with_message, require_admin_auth


def register_categories_routes(app):
    """Register categories routes"""
    
    @app.route("/api/categories", methods=["GET"])
    def get_active_categories():
        """Get all active categories (public endpoint)"""
        try:
            query = """
                SELECT 
                    c.name,
                    c.display_name
                FROM categories c
                WHERE c.is_active = 1
                ORDER BY c.name
            """
            categories = execute_query(query)
            data = {
                "success": True,
                "categories": categories or []
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
            print(f"Error fetching active categories: {str(e)}")
            traceback.print_exc()
            # Support JSONP even for errors
            callback = request.args.get('callback')
            if callback:
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({{'success': False, 'categories': []}});")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
            abort_with_message(500, f"Error fetching active categories: {str(e)}")
    
    @app.route("/api/admin/categories", methods=["GET", "POST"])
    @require_admin_auth
    def handle_categories():
        """Handle GET and POST requests for categories"""
        if request.method == "GET":
            return get_all_categories()
        elif request.method == "POST":
            return create_category()
    
    def get_all_categories():
        """Get all categories (admin endpoint - includes inactive categories)"""
        try:
            query = """
                SELECT 
                    c.id,
                    c.name,
                    c.display_name,
                    c.is_active,
                    c.created_at,
                    c.updated_at,
                    0 as properties_count
                FROM categories c
                ORDER BY c.name
            """
            categories = execute_query(query)
            
            # Convert datetime objects to ISO format strings for JSON serialization
            def convert_datetime_to_iso(obj):
                """Recursively convert datetime objects to ISO format strings"""
                if isinstance(obj, datetime):
                    return obj.isoformat()
                if isinstance(obj, dict):
                    return {k: convert_datetime_to_iso(v) for k, v in obj.items()}
                if isinstance(obj, list):
                    return [convert_datetime_to_iso(v) for v in obj]
                return obj
            
            # Convert datetime fields in categories data
            categories_data = [convert_datetime_to_iso(dict(category)) for category in categories] if categories else []
            
            # Return in the format expected by frontend: {categories: [...]}
            return jsonify({"categories": categories_data})
        except Exception as e:
            print(f"Error fetching all categories: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching all categories: {str(e)}")
    
    def create_category():
        """Create a new category"""
        try:
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
            # Validate required fields
            name = data.get('name')
            display_name = data.get('display_name')
            
            if not name:
                abort_with_message(400, "Category name is required")
            if not display_name:
                abort_with_message(400, "Category display_name is required")
            
            # Validate name length
            if len(name) > 100:
                abort_with_message(400, "Category name must be 100 characters or less")
            if len(display_name) > 250:
                abort_with_message(400, "Category display_name must be 250 characters or less")
            
            # Check if category with same name already exists
            existing = execute_query("SELECT id FROM categories WHERE name = %s", (name,))
            if existing:
                abort_with_message(400, f"Category with name '{name}' already exists")
            
            # Get optional fields
            is_active = data.get('is_active', True)
            is_active_int = 1 if is_active else 0
            
            # Insert new category
            insert_query = """
                INSERT INTO categories (name, display_name, is_active)
                VALUES (%s, %s, %s)
            """
            
            category_id = execute_insert(insert_query, (
                name,
                display_name,
                is_active_int
            ))
            
            # Return the created category directly (no re-fetch needed)
            category_data = {
                'id': category_id,
                'name': name,
                'display_name': display_name,
                'is_active': bool(is_active),
                'created_at': None,  # Will be set by DB, but not needed for response
                'updated_at': None,
                'properties_count': 0  # New category has no properties yet
            }
            
            return jsonify(category_data), 201
        except Exception as e:
            error_msg = str(e)
            print(f"Error creating category: {error_msg}")
            traceback.print_exc()
            # Check if it's a validation error (already has status code)
            if "already exists" in error_msg.lower() or "is required" in error_msg.lower() or "must be" in error_msg.lower():
                abort_with_message(400, error_msg)
            abort_with_message(500, f"Error creating category: {error_msg}")