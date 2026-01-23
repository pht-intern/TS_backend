"""
Unit types routes
"""
from flask import request, jsonify, make_response
from datetime import datetime
import json
import re
import traceback
from database import execute_query, execute_insert
from utils.helpers import abort_with_message, require_admin_auth


def register_unit_types_routes(app):
    """Register unit types routes"""
    
    @app.route("/api/unit-types", methods=["GET"])
    def get_active_unit_types():
        """Get all active unit types (public endpoint)"""
        try:
            query = """
                SELECT 
                    ut.name,
                    ut.display_name,
                    ut.bedrooms
                FROM unit_types ut
                WHERE ut.is_active = 1
                ORDER BY ut.bedrooms, ut.name
            """
            unit_types = execute_query(query)
            data = {
                "success": True,
                "unit_types": unit_types or []
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
            print(f"Error fetching active unit types: {str(e)}")
            traceback.print_exc()
            # Support JSONP even for errors
            callback = request.args.get('callback')
            if callback:
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', callback):
                    response = make_response(f"{callback}({{'success': False, 'unit_types': []}});")
                    response.headers['Content-Type'] = 'application/javascript'
                    return response
            return abort_with_message(500, f"Error fetching active unit types: {str(e)}")
    
    @app.route("/api/admin/unit-types", methods=["GET", "POST"])
    @require_admin_auth
    def handle_unit_types():
        """Handle GET and POST requests for unit types"""
        if request.method == "GET":
            return get_all_unit_types()
        elif request.method == "POST":
            return create_unit_type()
    
    def get_all_unit_types():
        """Get all unit types (admin endpoint - includes inactive unit types)"""
        try:
            query = """
                SELECT 
                    ut.id,
                    ut.name,
                    ut.display_name,
                    ut.bedrooms,
                    ut.is_active,
                    ut.created_at,
                    ut.updated_at,
                    (SELECT COUNT(*) FROM residential_properties rp WHERE rp.unit_type = ut.name AND rp.is_active = 1) as properties_count
                FROM unit_types ut
                ORDER BY ut.bedrooms, ut.name
            """
            unit_types = execute_query(query)
            
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
            
            # Convert datetime fields in unit_types data
            unit_types_data = [convert_datetime_to_iso(dict(unit_type)) for unit_type in unit_types] if unit_types else []
            
            # Return in the format expected by frontend: {unit_types: [...]}
            return jsonify({"unit_types": unit_types_data})
        except Exception as e:
            print(f"Error fetching all unit types: {str(e)}")
            traceback.print_exc()
            return abort_with_message(500, f"Error fetching all unit types: {str(e)}")
    
    def create_unit_type():
        """Create a new unit type"""
        try:
            # Better JSON parsing with error handling
            if not request.is_json:
                return abort_with_message(400, "Content-Type must be application/json")
            
            data = request.get_json(silent=True)
            if not data:
                return abort_with_message(400, "Invalid request data or empty JSON body")
            
            # Validate required fields
            name = data.get('name')
            display_name = data.get('display_name')
            bedrooms = data.get('bedrooms')
            
            if not name:
                return abort_with_message(400, "Unit type name is required")
            if not display_name:
                return abort_with_message(400, "Unit type display_name is required")
            
            # Validate name length
            if len(name) > 50:
                return abort_with_message(400, "Unit type name must be 50 characters or less")
            if len(display_name) > 250:
                return abort_with_message(400, "Unit type display_name must be 250 characters or less")
            
            # Handle bedrooms: make it optional, try to extract from name if not provided
            if bedrooms is None:
                # Try to extract bedrooms from name (e.g., "1BHK" -> 1, "2BHK" -> 2, "RK" -> 0)
                # Look for number at the start of the name
                match = re.match(r'^(\d+)', name.upper())
                if match:
                    bedrooms = int(match.group(1))
                else:
                    # Default to 0 if no number found (e.g., "RK", "STUDIO")
                    bedrooms = 0
            else:
                # Validate bedrooms is an integer if provided
                try:
                    bedrooms = int(bedrooms)
                    if bedrooms < 0:
                        return abort_with_message(400, "Bedrooms must be a non-negative integer")
                except (ValueError, TypeError):
                    return abort_with_message(400, "Bedrooms must be a valid integer")
            
            # Check if unit type with same name already exists
            existing = execute_query("SELECT id FROM unit_types WHERE name = %s", (name,))
            if existing:
                return abort_with_message(400, f"Unit type with name '{name}' already exists")
            
            # Get optional fields
            is_active = data.get('is_active', True)
            is_active_int = 1 if is_active else 0
            
            # Insert new unit type
            insert_query = """
                INSERT INTO unit_types (name, display_name, bedrooms, is_active)
                VALUES (%s, %s, %s, %s)
            """
            
            try:
                unit_type_id = execute_insert(insert_query, (
                    name,
                    display_name,
                    bedrooms,
                    is_active_int
                ))
            except Exception as db_error:
                error_msg = str(db_error).lower()
                # Handle duplicate key error (UNIQUE constraint violation)
                if "duplicate" in error_msg or "unique" in error_msg or "already exists" in error_msg:
                    return abort_with_message(400, f"Unit type with name '{name}' already exists")
                # Re-raise other database errors
                raise
            
            # Return the created unit type directly (no re-fetch needed)
            unit_type_data = {
                'id': unit_type_id,
                'name': name,
                'display_name': display_name,
                'bedrooms': bedrooms,
                'is_active': bool(is_active),
                'created_at': None,  # Will be set by DB, but not needed for response
                'updated_at': None,
                'properties_count': 0  # New unit type has no properties yet
            }
            
            return jsonify(unit_type_data), 201
        except Exception as e:
            error_msg = str(e)
            print(f"Error creating unit type: {error_msg}")
            traceback.print_exc()
            # Check if it's a validation error (already has status code)
            if "already exists" in error_msg.lower() or "is required" in error_msg.lower() or "must be" in error_msg.lower() or "must be a" in error_msg.lower() or "duplicate" in error_msg.lower() or "unique" in error_msg.lower():
                return abort_with_message(400, error_msg)
            return abort_with_message(500, f"Error creating unit type: {error_msg}")