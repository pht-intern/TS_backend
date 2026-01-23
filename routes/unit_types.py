"""
Unit types routes
"""
from flask import request, jsonify, make_response
from datetime import datetime
import json
import re
import traceback
from database import execute_query, execute_insert, execute_update
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
    
    # Define routes with path parameters BEFORE the base route
    # This ensures Flask matches the more specific routes first
    # IMPORTANT: This route must be defined before /api/admin/unit-types to ensure proper matching
    @app.route("/api/admin/unit-types/<int:unit_type_id>", methods=["GET", "PUT", "POST", "DELETE", "OPTIONS"])
    @require_admin_auth
    def handle_unit_type(unit_type_id):
        """Handle GET, PUT, POST, DELETE requests for a single unit type"""
        # Handle OPTIONS request for CORS preflight
        if request.method == "OPTIONS":
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Admin-Email'
            return response
        
        # Explicitly handle each method
        if request.method == "GET":
            return get_unit_type(unit_type_id)
        elif request.method in ["PUT", "POST"]:
            return update_unit_type(unit_type_id)
        elif request.method == "DELETE":
            return delete_unit_type(unit_type_id)
        
        # Fallback - should never reach here if route is configured correctly
        return abort_with_message(405, f"Method {request.method} not allowed for this endpoint")
    
    def get_unit_type(unit_type_id):
        """Get a single unit type by ID"""
        try:
            query = """
                SELECT 
                    ut.id,
                    ut.name,
                    ut.display_name,
                    ut.bedrooms,
                    ut.is_active
                FROM unit_types ut
                WHERE ut.id = %s
            """
            result = execute_query(query, (unit_type_id,))
            if not result:
                abort_with_message(404, "Unit type not found")
            
            unit_type = dict(result[0])
            # Convert is_active from int to bool
            if 'is_active' in unit_type:
                unit_type['is_active'] = bool(unit_type['is_active'])
            
            return jsonify({
                "success": True,
                "unit_type": unit_type
            })
        except Exception as e:
            print(f"Error fetching unit type: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching unit type: {str(e)}")
    
    def update_unit_type(unit_type_id):
        """Update a unit type"""
        try:
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
            # Validate required fields
            display_name = data.get('display_name', '').strip()
            is_active = data.get('is_active', True)
            
            if not display_name:
                abort_with_message(400, "display_name is required")
            
            # Validate display_name length
            if len(display_name) > 250:
                abort_with_message(400, "Unit type display_name must be 250 characters or less")
            
            # Convert is_active to int
            is_active_int = 1 if is_active else 0
            
            # Update unit type
            update_query = "UPDATE unit_types SET display_name = %s, is_active = %s, updated_at = NOW() WHERE id = %s"
            affected_rows = execute_update(update_query, (display_name, is_active_int, unit_type_id))
            
            if affected_rows == 0:
                abort_with_message(404, "Unit type not found")
            
            return jsonify({
                "success": True,
                "message": "Unit type updated successfully"
            })
        except Exception as e:
            error_msg = str(e)
            print(f"Error updating unit type: {error_msg}")
            traceback.print_exc()
            # Check if it's a validation error
            if "is required" in error_msg.lower() or "must be" in error_msg.lower():
                abort_with_message(400, error_msg)
            abort_with_message(500, f"Error updating unit type: {error_msg}")
    
    def delete_unit_type(unit_type_id):
        """Delete a unit type"""
        try:
            # First check if unit type exists
            check_query = "SELECT id FROM unit_types WHERE id = %s"
            existing = execute_query(check_query, (unit_type_id,))
            if not existing:
                abort_with_message(404, "Unit type not found")
            
            # Check if unit type has associated properties (optional safety check)
            # This is a soft check - we'll still allow deletion but warn if there are properties
            # You can uncomment and modify this if you want to prevent deletion when properties exist
            # residential_count = execute_query(
            #     "SELECT COUNT(*) as count FROM residential_properties WHERE unit_type = (SELECT name FROM unit_types WHERE id = %s) AND is_active = 1",
            #     (unit_type_id,)
            # )
            # total_count = residential_count[0]['count'] if residential_count else 0
            # if total_count > 0:
            #     abort_with_message(400, f"Cannot delete unit type: {total_count} properties are associated with this unit type")
            
            # Delete unit type
            delete_query = "DELETE FROM unit_types WHERE id = %s"
            affected_rows = execute_update(delete_query, (unit_type_id,))
            
            if affected_rows == 0:
                abort_with_message(404, "Unit type not found")
            
            return jsonify({
                "success": True,
                "message": "Unit type deleted successfully"
            })
        except Exception as e:
            error_msg = str(e)
            print(f"Error deleting unit type: {error_msg}")
            traceback.print_exc()
            abort_with_message(500, f"Error deleting unit type: {error_msg}")
    
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